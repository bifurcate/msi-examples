#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import plotly.graph_objects as go

parser = argparse.ArgumentParser(description="Aggregate prime data and generate Ulam spiral")

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


def ulam_spiral_coords(max_n):
    """Generate (x, y) coordinates for numbers 1..max_n in an Ulam spiral."""
    coords = {}
    x, y = 0, 0
    dx, dy = 1, 0  # Start moving right
    steps_in_direction = 1
    steps_taken = 0
    turns = 0

    for n in range(1, max_n + 1):
        coords[n] = (x, y)
        x += dx
        y += dy
        steps_taken += 1

        if steps_taken == steps_in_direction:
            steps_taken = 0
            # Turn left: (dx, dy) -> (-dy, dx)
            dx, dy = -dy, dx
            turns += 1
            if turns % 2 == 0:
                steps_in_direction += 1

    return coords


def main():
    all_primes = set()
    max_n = 0

    for work_dir in sorted(root_dir.iterdir()):
        if work_dir.is_dir():
            data_file = work_dir / "data.json"
            if data_file.exists():
                try:
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                    all_primes.update(data["primes"])
                    if debug:
                        print(f"Loaded {len(data['primes'])} primes from {work_dir.name}")
                except Exception as e:
                    print(f"Error loading data from {work_dir.name}: {e}")

            config_file = work_dir / "config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                max_n = max(max_n, config.get("max_n", config.get("end", 0)))

    print(f"Found {len(all_primes)} primes up to {max_n}")

    # Generate Ulam spiral coordinates
    coords = ulam_spiral_coords(max_n)

    # Separate primes and composites
    prime_x = [coords[n][0] for n in range(1, max_n + 1) if n in all_primes]
    prime_y = [coords[n][1] for n in range(1, max_n + 1) if n in all_primes]
    prime_labels = [str(n) for n in range(1, max_n + 1) if n in all_primes]

    composite_x = [coords[n][0] for n in range(1, max_n + 1) if n not in all_primes]
    composite_y = [coords[n][1] for n in range(1, max_n + 1) if n not in all_primes]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=composite_x, y=composite_y,
        mode='markers',
        marker=dict(size=2, color='lightgray', opacity=0.3),
        name='Composite',
        hoverinfo='skip',
    ))

    fig.add_trace(go.Scatter(
        x=prime_x, y=prime_y,
        mode='markers',
        marker=dict(size=3, color='blue', opacity=0.7),
        name='Prime',
        text=prime_labels,
        hovertemplate='%{text}<extra></extra>',
    ))

    fig.update_layout(
        title=f'Ulam Spiral (n = {max_n})',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor='x'),
        plot_bgcolor='white',
        width=1400,
        height=1400,
    )

    plot_path = root_dir / 'ulam_spiral.html'
    fig.write_html(str(plot_path))
    print(f"Plot saved to {plot_path}")

    # Prime counting function π(n)
    ns = list(range(1, max_n + 1))
    pi = []
    count = 0
    for n in ns:
        if n in all_primes:
            count += 1
        pi.append(count)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=ns, y=pi,
        mode='lines',
        line=dict(color='blue', width=1),
        name='π(n)',
    ))
    fig2.update_layout(
        title='Prime Counting Function π(n)',
        xaxis_title='n',
        yaxis_title='π(n)',
        width=1000,
        height=600,
    )

    plot_path2 = root_dir / 'prime_counting.html'
    fig2.write_html(str(plot_path2))
    print(f"Plot saved to {plot_path2}")

if __name__ == "__main__":
    main()
