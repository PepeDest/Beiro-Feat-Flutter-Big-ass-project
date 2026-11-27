"""Runner for the long jobs of niches D, F and G (docs/ROADMAP_DI.md). Uses all cores of the machine.

    python cluster/run_cluster.py --smoke              # a short test (a few minutes)
    python cluster/run_cluster.py                      # all jobs: d1 d2 f g3
    python cluster/run_cluster.py --part 1/2           # half of the tasks (machine 1 of 2)
    python cluster/run_cluster.py --jobs d1,g3         # only some jobs
    python cluster/run_cluster.py --pack               # make the zip of the results

Each finished task is saved at once in cluster_out/<job>/<task>.json. If the run stops, start the same command again:
the runner skips the finished tasks. The progress is in cluster_out/progress.log.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")                      # one thread for each worker process

import argparse, hashlib, json, pathlib, platform, socket, sys, time, traceback, zipfile
from concurrent.futures import ProcessPoolExecutor, as_completed

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "experiments")); sys.path.insert(0, str(ROOT / "src"))
JOBS = {"d1": "e27_d_rochester", "d2": "e27_d_rochester", "f": "e28_f_cld_map", "g3": "e29_g_te_dt"}


def module(job):
    import importlib
    return importlib.import_module(JOBS[job])


def _work(args):
    job, task, out_dir = args
    t0 = time.time()
    try:
        res = module(job).run_task(task)
        rec = dict(task=task, result=res, seconds=time.time() - t0, host=socket.gethostname())
        f = pathlib.Path(out_dir, job, task["name"] + ".json")
        tmp = f.with_suffix(".tmp")
        tmp.write_text(json.dumps(rec))
        os.replace(tmp, f)                                 # atomic: a file is complete or absent
        return task["name"], time.time() - t0, None
    except Exception:
        return task["name"], time.time() - t0, traceback.format_exc()


def in_part(name, part):
    k, n = part
    return int(hashlib.sha1(name.encode()).hexdigest(), 16) % n == k - 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", default="d1,d2,f,g3")
    ap.add_argument("--part", default="1/1")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "cluster_out"))
    ap.add_argument("--pack", action="store_true")
    a = ap.parse_args()
    out = pathlib.Path(a.out + ("_smoke" if a.smoke else ""))
    if a.pack:
        return pack(out)
    part = tuple(int(x) for x in a.part.split("/"))
    jobs = [j for j in a.jobs.split(",") if j]
    todo, n_all = [], 0
    for job in dict.fromkeys(jobs):
        (out / job).mkdir(parents=True, exist_ok=True)
        for t in module(job).tasks(smoke=a.smoke) if job not in ("d1", "d2") else \
                [t for t in module(job).tasks(smoke=a.smoke) if t["job"] == job]:
            if not in_part(t["name"], part):
                continue
            n_all += 1
            if not (out / job / (t["name"] + ".json")).exists():
                todo.append((job, t))
    todo.sort(key=lambda jt: -jt[1]["cost"])               # longest tasks first
    total_cost = sum(t["cost"] for _, t in todo)
    log = open(out / "progress.log", "a", encoding="utf-8")
    def say(s):
        line = time.strftime("%Y-%m-%d %H:%M:%S ") + s
        print(line, flush=True); log.write(line + "\n"); log.flush()
    say(f"host {socket.gethostname()} | {platform.platform()} | python {platform.python_version()} | "
        f"workers {a.workers} | part {a.part} | jobs {jobs}")
    say(f"tasks in this part: {n_all}, already done: {n_all - len(todo)}, to do: {len(todo)}. "
        f"Rough estimate: {total_cost / 3600 / max(a.workers, 1):.1f} hours on {a.workers} workers "
        f"(the estimate assumes a core as fast as the test PC)")
    (out / "machine.json").write_text(json.dumps(dict(host=socket.gethostname(), platform=platform.platform(),
                                                      cpus=os.cpu_count(), workers=a.workers, part=a.part,
                                                      jobs=jobs, smoke=a.smoke)))
    t0, done_cost, n_ok, n_err = time.time(), 0.0, 0, 0
    with ProcessPoolExecutor(a.workers) as ex:
        futs = {ex.submit(_work, (job, t, str(out))): t for job, t in todo}
        for f in as_completed(futs):
            t = futs[f]
            name, sec, err = f.result()
            done_cost += t["cost"]
            if err:
                n_err += 1
                say(f"ERROR in {name}:\n{err}")
            else:
                n_ok += 1
            el = time.time() - t0
            eta = el / max(done_cost, 1e-9) * (total_cost - done_cost)
            if n_ok % 50 == 0 or err or n_ok + n_err == len(todo):
                say(f"{n_ok + n_err}/{len(todo)} done ({n_err} errors), {el / 3600:.2f} h passed, "
                    f"about {eta / 3600:.1f} h left")
    say(f"finished: {n_ok} tasks done, {n_err} errors. Next: python cluster/run_cluster.py --pack"
        + (" --smoke" if a.smoke else ""))


def pack(out):
    host = socket.gethostname()
    z = ROOT / f"results_{out.name}_{host}.zip"
    n = 0
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in out.rglob("*"):
            if f.is_file() and f.suffix in (".json", ".log"):
                zf.write(f, f.relative_to(out.parent)); n += 1
    print(f"wrote {z} with {n} files. Send this file back.")


if __name__ == "__main__":
    main()
