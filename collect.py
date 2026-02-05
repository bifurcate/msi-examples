import argparse
import json
from pathlib import Path
import pandas as pd
import plotly.express as px

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
    
    # Create interactive scatterplot with Plotly
    fig = px.scatter(
        df,
        x='manifold_volume',
        y='margulis_number',
        color='number_cusps',
        hover_data={'manifold_identifier': True, 'manifold_volume': ':.4f', 'margulis_number': ':.4f', 'number_cusps': True},
        color_continuous_scale='Viridis',
        labels={
            'manifold_volume': 'Manifold Volume',
            'margulis_number': 'Margulis Number',
            'number_cusps': 'Number of Cusps'
        },
        title='Margulis Number vs Manifold Volume'
    )
    
    fig.update_traces(marker=dict(size=5, opacity=0.7))
    
    # Save plot as HTML
    plot_path = root_dir / 'scatterplot.html'
    fig.write_html(str(plot_path))
    print(f"\nPlot saved to {plot_path}")

if __name__ == "__main__":
    main()
