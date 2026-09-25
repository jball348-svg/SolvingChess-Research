from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import jsonschema
import pytest

PROJECT = Path(__file__).resolve().parents[1]


def load_json(relative: str) -> dict:
    return json.loads((PROJECT / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def repository_validator():
    path = PROJECT / "scripts" / "validation" / "validate_repository.py"
    spec = importlib.util.spec_from_file_location("bootstrap_validate_repository", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_repository


@pytest.mark.parametrize(
    "schema_path",
    sorted((PROJECT / "schemas").glob("*.schema.json")),
    ids=lambda path: path.name,
)
def test_governance_schema_is_valid_draft_2020_12(schema_path: Path) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)


@pytest.mark.parametrize(
    ("instance_path", "schema_path"),
    [
        ("state/ARTIFACT_REGISTRY.json", "schemas/artifact_registry.schema.json"),
        ("state/AUTONOMY_STATE.json", "schemas/autonomy_state.schema.json"),
        ("state/PROGRAM_STATE.json", "schemas/program_state.schema.json"),
        ("state/REFERENCE_REGISTRY.json", "schemas/reference_registry.schema.json"),
    ],
)
def test_current_governance_instance_validates(
    instance_path: str, schema_path: str
) -> None:
    validator = jsonschema.Draft202012Validator(load_json(schema_path))
    errors = sorted(
        validator.iter_errors(load_json(instance_path)),
        key=lambda error: list(error.absolute_path),
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in errors
    )


def completion(status: str = "PASS") -> dict:
    passed = status == "PASS"
    return {
        "schema_version": "1.0.0",
        "run_id": "schema-test-G14-attempt-1",
        "programme": "G14",
        "status": status,
        "gate_result": status,
        "state_transition": {"from": "G13", "to": "G14"},
        "handoff_path": "research/G14/G14_Technical_Handoff.md",
        "freeze_manifest_path": "research/G14/G14_Freeze_Manifest.json",
        "program_state_path": "state/PROGRAM_STATE.json",
        "tests_run": [],
        "validation_summary": {
            "result": "PASS" if passed else status,
            "checks": ["schema regression fixture"],
        },
        "blockers": [] if passed else ["synthetic schema fixture blocker"],
        "next_programme": "G15" if passed else "G14",
        "next_programme_authorized": False,
        "human_input_required": False,
        "human_input_reason": None,
        "final_summary": "Synthetic schema-only completion record.",
    }


@pytest.mark.parametrize("status", ["PASS", "HOLD", "BLOCKED", "FAILED"])
def test_completion_schema_accepts_each_scientific_status(status: str) -> None:
    value = completion(status)
    jsonschema.Draft202012Validator(
        load_json("schemas/g_completion.output.schema.json")
    ).validate(value)
    jsonschema.Draft202012Validator(
        load_json("schemas/g_completion.schema.json")
    ).validate(value)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["state_transition"].update({"from": "G12"}),
        lambda value: value.update({"next_programme": "G16"}),
        lambda value: value.update({"gate_result": "HOLD"}),
        lambda value: value.update({"handoff_path": None}),
    ],
)
def test_completion_schema_rejects_invalid_transition_or_closeout(mutation) -> None:
    value = completion()
    mutation(value)
    errors = list(
        jsonschema.Draft202012Validator(
            load_json("schemas/g_completion.schema.json")
        ).iter_errors(value)
    )
    assert errors


def test_completion_schema_enforces_terminal_g42() -> None:
    value = completion()
    value.update(
        {
            "programme": "G42",
            "state_transition": {"from": "G41", "to": "G42"},
            "next_programme": None,
            "next_programme_authorized": False,
        }
    )
    validator = jsonschema.Draft202012Validator(
        load_json("schemas/g_completion.schema.json")
    )
    validator.validate(value)
    invalid = copy.deepcopy(value)
    invalid["next_programme_authorized"] = True
    assert list(validator.iter_errors(invalid))


def test_output_admission_does_not_replace_strict_transition_validation() -> None:
    value = completion()
    value["next_programme"] = "G16"
    jsonschema.Draft202012Validator(
        load_json("schemas/g_completion.output.schema.json")
    ).validate(value)
    strict = jsonschema.Draft202012Validator(
        load_json("schemas/g_completion.schema.json")
    )
    assert list(strict.iter_errors(value))


def test_output_admission_requires_complete_response_shape() -> None:
    value = completion()
    value.pop("final_summary")
    output = jsonschema.Draft202012Validator(
        load_json("schemas/g_completion.output.schema.json")
    )
    assert list(output.iter_errors(value))


def test_programme_state_hashes_control_original_authority_bytes() -> None:
    state = load_json("state/PROGRAM_STATE.json")
    bindings = [
        (
            state["permanent_roadmap"]["path"],
            state["permanent_roadmap"]["original_path"],
            state["permanent_roadmap"]["sha256"],
        ),
        (
            state["latest_frozen_handoff"]["path"],
            state["latest_frozen_handoff"]["original_path"],
            state["latest_frozen_handoff"]["sha256"],
        ),
    ]
    contracts = state["active_contracts"]
    for value in (
        contracts["rules"],
        contracts["state_serialization"],
        contracts["compute"],
        *contracts["proof_certificate_contracts"],
    ):
        bindings.append(
            (
                value["authority_path"],
                value["original_authority_path"],
                value["sha256"],
            )
        )
    for normalized, original, expected in bindings:
        assert (PROJECT / normalized).is_file()
        assert sha256(PROJECT / original) == expected


def test_programme_state_binds_registry_bytes() -> None:
    state = load_json("state/PROGRAM_STATE.json")
    registries = state["registries"]
    assert sha256(PROJECT / registries["artifact_registry_path"]) == registries[
        "artifact_registry_sha256"
    ]
    assert sha256(PROJECT / registries["reference_registry_path"]) == registries[
        "reference_registry_sha256"
    ]


def test_programme_state_bootstrap_readiness_is_consistent() -> None:
    validator = jsonschema.Draft202012Validator(
        load_json("schemas/program_state.schema.json")
    )
    accepted = load_json("state/PROGRAM_STATE.json")
    accepted["repository_bootstrap"].update(
        {
            "completion_status": "COMPLETE",
            "autonomous_loop_readiness": "READY",
        }
    )
    validator.validate(accepted)
    contradictory = copy.deepcopy(accepted)
    contradictory["repository_bootstrap"]["autonomous_loop_readiness"] = "NOT_READY"
    assert list(validator.iter_errors(contradictory))


def test_programme_state_frozen_git_identity_is_coherent() -> None:
    validator = jsonschema.Draft202012Validator(
        load_json("schemas/program_state.schema.json")
    )
    state = load_json("state/PROGRAM_STATE.json")
    state["last_frozen_git"] = {
        "status": "FROZEN",
        "commit": "a" * 40,
        "tag": "bootstrap-v1.0.0",
    }
    validator.validate(state)
    state["last_frozen_git"]["commit"] = None
    assert list(validator.iter_errors(state))


def test_research_tree_matches_programme_state() -> None:
    files = {
        path.relative_to(PROJECT).as_posix()
        for path in (PROJECT / "research" / "G14").rglob("*")
        if path.is_file()
    }
    state = load_json("state/PROGRAM_STATE.json")
    latest = state["latest_completed_programme"]["number"]
    if latest < 14:
        assert files == {"research/G14/README.md"}
    else:
        assert {
            "research/G14/README.md",
            "research/G14/G14_Completion.json",
            "research/G14/G14_Freeze_Manifest.json",
            "research/G14/G14_Technical_Handoff.md",
        } <= files
    assert not (PROJECT / "research" / "G15").exists()


def test_repository_acceptance_validator_matches_launch_authorization() -> None:
    result = repository_validator()(PROJECT, require_clean=False)
    state = load_json("state/PROGRAM_STATE.json")
    next_programme = state["next_programme"]
    if next_programme["authorized"]:
        assert result["valid"], "\n".join(result["errors"])
    else:
        assert not result["valid"]
        assert result["errors"] == [
            f"{next_programme['programme']} is not authorized"
        ]
