"""RP3-MR1 final rerun: frozen RP3 procedure with verified durable I/O only."""
import argparse
import os
from pathlib import Path
import rp2
import rp3
from model import encoded
from rp3_durable_v2 import write_json, validate, sync_directory


class Run(rp3.Run):
    def __init__(self, args):
        super().__init__(args)
        self.report.update(experiment='RP3-MR1-FINAL', original_experiment='BLOCKED',
                           measurement_role='replacement' if args.rung == 'r2' else 'continuation')
        self.journal = (self.directory/'rows.jsonl').open('x')
        self.journaled = 0

    def emit(self, event):
        super().emit(event)
        if sum(self.event_counts.values()) % 32 == 0:
            os.fsync(self.events.fileno())

    def checkpoint(self):
        if not self.events.closed:
            self.events.flush()
            os.fsync(self.events.fileno())
        for row in self.report['rows'][self.journaled:]:
            if 'fallback_residual' not in row:
                break
            self.journal.write(encoded(row)+'\n')
            self.journaled += 1
        self.journal.flush()
        os.fsync(self.journal.fileno())
        write_json(self.args.output, self.report)

    def finish(self):
        self.events.flush()
        os.fsync(self.events.fileno())
        super().finish()
        self.journal.close()
        # Re-emit the final in-memory report after the frozen RP2 finish has
        # returned, then read it back before publishing the completion marker.
        # The marker is written only after two independent complete validations.
        self.report['durability_check'] = 'post-replace-readback-v2'
        write_json(self.args.output, self.report)
        completion = validate(self.directory, marker=False)
        write_json(self.directory/'completion.json', completion)
        validate(self.directory)
        sync_directory(self.directory)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['acquire','evaluate'])
    p.add_argument('--rung', choices=['r2','r3','r4'], required=True)
    p.add_argument('--arm', choices=list('BCFG'), required=True)
    p.add_argument('--repeat', type=int, choices=[1,2,3], required=True)
    p.add_argument('--diagnostic', choices=['primary','ablation','reverse'], default='primary')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--freeze', type=Path, required=True)
    p.add_argument('--source-freeze', type=Path, required=True)
    a = p.parse_args(); a.output = a.output.resolve()
    if a.mode == 'acquire' and (a.rung != 'r3' or a.arm not in 'CG' or a.diagnostic != 'primary'):
        p.error('MR1 permits only the remaining R3 C/G acquisition')
    if a.diagnostic != 'primary' and (a.rung == 'r2' or (a.diagnostic == 'ablation' and a.arm != 'G')):
        p.error('invalid diagnostic')
    if a.output.exists():
        p.error('refusing to overwrite existing output')
    a.output.parent.mkdir(parents=True, exist_ok=True)
    from measure import limits
    limits()
    # Replace persistence functions, leaving every frozen source byte intact.
    rp2.write_json = rp3.write_json = write_json
    run = Run(a)
    try:
        getattr(run, a.mode)()
        run.finish()
    except Exception as exc:
        run.report.update(status='BLOCKED', error=type(exc).__name__+': '+str(exc),
                          partial_cost=run.meter.elapsed(run.begin))
        if not run.journal.closed:
            run.checkpoint()
        raise


if __name__ == '__main__':
    main()
