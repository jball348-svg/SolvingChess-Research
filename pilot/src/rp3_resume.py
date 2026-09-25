"""Operational continuation after recorded checkpoint recovery.

The experiment driver and original campaign source remain byte-for-byte frozen.
This copies its schedule, changing only already-completed run/freeze handling.
No primary measurement is overwritten or repeated.
"""
from rp3_campaign import *

def campaign(output, source):
    frozen = read(source)
    for path,digest in frozen['driver_sources'].items(): assert file_hash(ROOT/path)==digest,path
    for path,digest in frozen['inherited_rp2_files'].items(): assert file_hash(ROOT/path)==digest,path
    sequence = read(output/'sequence.json')
    cpu = sum(e['cpu_s'] for e in sequence)
    current = ROOT/'pilot/evidence/rp2/donor-freeze.json'
    def execute(mode,rung,arm,repeat,diagnostic='primary'):
        nonlocal cpu
        label=f'{mode}-{rung}-{diagnostic}-{repeat}-{arm}'
        directory=output/label
        if directory.exists():
            recorded = next(e for e in sequence if e['label']==label)
            env = read(directory/'envelope.json')
            report = read(directory/'report.json')
            assert env['returncode']==recorded['returncode']==0 and report['status']=='COMPLETE'
            assert env['cpu_s']==recorded['cpu_s'] and env['wall_s']==recorded['wall_s']
            return  # Existing expense remains; do not run this process again.
        command=[sys.executable,'pilot/src/measure.py','--output',str(directory/'envelope.json'),'--',
                 sys.executable,'pilot/src/rp3.py',mode,'--rung',rung,'--arm',arm,'--repeat',str(repeat),
                 '--diagnostic',diagnostic,'--output',str(directory/'report.json'),
                 '--freeze',str(current),'--source-freeze',str(source)]
        process=subprocess.run(command,text=True,capture_output=True)
        env=read(directory/'envelope.json');cpu+=env['cpu_s']
        sequence.append(dict(label=label,command=command,returncode=process.returncode,
            cpu_s=env['cpu_s'],wall_s=env['wall_s'],recorded_utc=now()))
        write_json(output/'sequence.json',sequence)
        print(json.dumps(sequence[-1]),flush=True)
        if cpu>4*3600: raise RuntimeError('RP3 CPU budget exhausted; expenses retained')
        if process.returncode:
            # A process exhaustion remains a measured UNKNOWN; no selective rerun.
            # Cannot silently publish a partial, unreproducible acquisition library.
            if mode=='acquire' or read(directory/'report.json').get('status')=='BLOCKED':
                raise RuntimeError('BLOCKED: '+label+'; '+env.get('stderr','')[-1500:])
        if sum(p.stat().st_size for p in output.rglob('*') if p.is_file())>1024**3:
            raise RuntimeError('RP3 disk budget exhausted')
    for previous,next_rung in [('r1','r2'),('r2','r3'),('r3','r4')]:
        for repeat,order in enumerate(['BCFG','CFGB','FGBC'],1):
            for arm in order:
                if arm in 'CG':execute('acquire',previous,arm,repeat)
        update=dict(schema=1,rung=previous,usable_at=next_rung,frozen_utc=now(),
            source_freeze_sha256=file_hash(source),parent_freeze_sha256=file_hash(current),acquisitions={},
            evidence_files={})
        information=set()
        for arm in 'CG':
            identities=set();work=set()
            for repeat in [1,2,3]:
                directory=output/f'acquire-{previous}-primary-{repeat}-{arm}'
                r=read(directory/'report.json')
                assert r['status']=='COMPLETE'
                information.add(tuple((x['query_id'],x['certificate_sha256']) for x in r['rows']))
                identities.add(r['library_sha256']);work.add(json.dumps(stable(r),sort_keys=True))
                update['acquisitions'][f'{repeat}-{arm}']={k:r[k] for k in ['library_path','library_sha256','library_serialized_bytes','object_ids','query_sha256','initial_entries','new_entries']}
                for path in directory.rglob('*'):
                    if path.is_file():update['evidence_files'][str(path.relative_to(ROOT))]=file_hash(path)
            assert len(identities)==len(work)==1,'nonreproducible update '+arm
        assert len(information)==1,'C/G training information differs'
        current=output/f'freeze-after-{previous}.json'
        if current.exists():
            existing=read(current)
            assert {k:v for k,v in update.items() if k!='frozen_utc'} == {k:v for k,v in existing.items() if k!='frozen_utc'}
        else:
            write_json(current,update)
        print(json.dumps(dict(freeze=str(current),sha256=file_hash(current),objects={a:len(update['acquisitions']['1-'+a]['object_ids']) for a in 'CG'})),flush=True)
        for repeat,order in enumerate(['BCFG','CFGB','FGBC'],1):
            for arm in order:execute('evaluate',next_rung,arm,repeat)
        if next_rung in ['r3','r4']:
            for repeat in [1,2,3]:execute('evaluate',next_rung,'G',repeat,'ablation')
            for repeat,order in enumerate(['BCFG','CFGB','FGBC'],1):
                for arm in order:execute('evaluate',next_rung,arm,repeat,'reverse')
    print(json.dumps(dict(status='RP3_EXECUTION_COMPLETE',processes=len(sequence),actual_cpu_s=cpu,final_freeze=str(current))))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--source-freeze',type=Path,required=True)
    a=p.parse_args()
    campaign(a.output.resolve(),a.source_freeze.resolve())
