import argparse
import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

parser = argparse.ArgumentParser(description="Collect data from generated manifold directories")

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
    data_list = []
    
    # Iterate through all directories in root_dir
    for work_dir in sorted(root_dir.iterdir()):
        if work_dir.is_dir():
            data_file = work_dir / "data.json"
            if data_file.exists():
                try:
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                    data_list.append(data)
                    if debug:
                        print(f"Loaded data from {work_dir.name}")
                except Exception as e:
                    print(f"Error loading data from {work_dir.name}: {e}")
    
    # Create pandas dataframe
    df = pd.DataFrame(data_list)
    
    # Print the combined dataframe
    print(df)
    
    # Create scatterplot
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df['manifold_volume'], df['margulis_number'], alpha=0.5, s=10, c=df['number_cusps'], cmap='viridis')
    plt.xlabel('Manifold Volume')
    plt.ylabel('Margulis Number')
    plt.title('Margulis Number vs Manifold Volume')
    cbar = plt.colorbar(scatter, label='Number of Cusps')
    cbar.locator = MaxNLocator(integer=True)
    cbar.update_ticks()
    plt.grid(True, alpha=0.3)
    
    # Save plot as SVG
    plot_path = root_dir / 'scatterplot.svg'
    plt.savefig(plot_path, format='svg')
    print(f"\nPlot saved to {plot_path}")

if __name__ == "__main__":
    main()
