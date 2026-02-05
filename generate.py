import argparse
from pathlib import Path
import snappy

parser = argparse.ArgumentParser(description="Generate parameters")

parser.add_argument(
    '-d', '--debug-mode',
    action='store_true',
    help="Enable debug mode",
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
    for manifold in snappy.OrientableCuspedCensus[:5000]:
        work_dir = root_dir / manifold.name()
        Path(work_dir).mkdir(exist_ok=True)
        print(f"Generated work directory: {work_dir}")

if __name__ == "__main__":
    main()