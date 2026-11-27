"""Build the zip for the Xeon machines: python cluster/make_bundle.py (from the repository root)."""
import hashlib, pathlib, time, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
FILES = (["cluster/run_cluster.py", "cluster/requirements.txt", "cluster/run_linux.sh", "cluster/run_windows.bat",
          "cluster/LEGGIMI.md", "cluster/README.md", "cluster/data/f_units.json",
          "experiments/e27_d_rochester.py", "experiments/e28_f_cld_map.py", "experiments/e29_g_te_dt.py",
          "docs/D.md", "docs/F.md", "docs/G.md", "docs/ROADMAP_DI.md"]
         + sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "src" / "vlife").glob("*.py")))


def main():
    name = f"cluster_bundle_{time.strftime('%Y%m%d')}"
    z = ROOT / f"{name}.zip"
    sums = []
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in FILES:
            data = (ROOT / f).read_bytes()
            sums.append(f"{hashlib.sha256(data).hexdigest()}  {f}")
            info = zipfile.ZipInfo(f"{name}/{f}", date_time=(2026, 11, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if f.endswith(".sh") else 0o644) << 16
            zf.writestr(info, data)
        zf.writestr(f"{name}/SHA256SUMS.txt", "\n".join(sums) + "\n")
    h = hashlib.sha256(z.read_bytes()).hexdigest()
    print(f"wrote {z} ({z.stat().st_size / 1e6:.2f} MB), {len(FILES)} files, sha256 {h}")


if __name__ == "__main__":
    main()
