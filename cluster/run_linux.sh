#!/usr/bin/env bash
# Start the long jobs on a Linux machine. Usage, from the folder of the zip:
#   nohup bash cluster/run_linux.sh > run.log 2>&1 &
# For two machines: bash cluster/run_linux.sh --part 1/2 on the first, --part 2/2 on the second.
set -e
cd "$(dirname "$0")/.."
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r cluster/requirements.txt
python cluster/run_cluster.py --smoke
python cluster/run_cluster.py "$@"
python cluster/run_cluster.py --pack
