import snappy
import json
from pathlib import Path

def run(work_dir):
    manifold_identifier = str(work_dir.name)
    manifold = snappy.Manifold(manifold_identifier)
    number_cusps = int(manifold.num_cusps())
    margulis_number = float(manifold.margulis())
    manifold_volume = float(manifold.volume())

    with open(work_dir / "output.txt", "w") as f:
        f.write(f"Manifold Identifier: {manifold_identifier}\n")
        f.write(f"Margulis number: {margulis_number}\n")
        f.write(f"Number of cusps: {number_cusps}\n")
        f.write(f"Manifold Volume: {manifold_volume}\n")
    
    # Save data to JSON file
    data = {
        "manifold_identifier": manifold_identifier,
        "number_cusps": number_cusps,
        "margulis_number": margulis_number,
        "manifold_volume": manifold_volume
    }
    with open(work_dir / "data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("Running func.run on", work_dir.name)