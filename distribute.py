#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(description="Partition natural numbers into partitions for primality testing")

parser.add_argument(
    '-d', '--debug-mode',
    action='store_true',
    help="Enable debug mode",
)

parser.add_argument(
    '--max-n',
    type=int,
    default=10000,
    help="Highest natural number to consider (default: 10000)"
)

parser.add_argument(
    '--partition-size',
    type=int,
    default=1000,
    help="Size of each partition (default: 1000)"
)

parser.add_argument(
    'root_dir',
    nargs='?',
    default='.',
    type=str,
    help="Name of the root run directory"
)

args = parser.parse_args()
debug = args.debug_mode
root_dir = Path(args.root_dir)

def main():
    max_n = args.max_n
    partition_size = args.partition_size

    root_dir.mkdir(parents=True, exist_ok=True)
    msi_run_src = Path(__file__).parent / "msi-run.sh"
    if msi_run_src.exists():
        shutil.copy2(msi_run_src, root_dir / "msi-run.sh")

    partition_id = 0
    start = 2
    while start <= max_n:
        end = min(start + partition_size - 1, max_n)
        work_dir = root_dir / f"partition_{start}_{end}"
        work_dir.mkdir(parents=True, exist_ok=True)

        config = {
            "partition_id": partition_id,
            "start": start,
            "end": end,
            "max_n": max_n,
        }
        with open(work_dir / "config.json", "w") as f:
            json.dump(config, f, indent=2)

        if debug:
            print(f"Distributed work directory: {work_dir} (range {start}-{end})")
        else:
            print(f"Distributed work directory: {work_dir}")

        start = end + 1
        partition_id += 1

if __name__ == "__main__":
    main()
