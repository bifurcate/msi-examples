# MSI Examples

A parallel computing workflow for experimental mathematics, designed for execution on MSI (Minnesota Supercomputing Institute).

## Setup

```bash
poetry install
```

## Distribute-Work-Aggregate Pipeline

The pipeline splits a computation into independent partitions that can be processed in parallel, then aggregates the results. It has three stages:

### 1. Distribute (`distribute.py`)

Partitions the problem space and creates a subdirectory per partition under a root directory. Each subdirectory contains a `config.json` with the partition parameters.

```bash
poetry run python distribute.py [options] <root_dir>
```

| Option | Default | Description |
|---|---|---|
| `--max-n` | 10000 | Highest natural number to consider |
| `--partition-size` | 1000 | Size of each partition |
| `-d, --debug-mode` | off | Print partition ranges |

Example output structure:

```
my-run/
  partition_2_1001/config.json
  partition_1002_2001/config.json
  ...
```

### 2. Execute (`worker.py` + `execute.py`)

The worker loops over partition subdirectories and atomically claims unclaimed ones using filesystem atomics (`os.O_CREAT | os.O_EXCL` on a `.claimed` file). This allows multiple workers to run concurrently against the same directory without any external coordination. For each claimed partition, the worker calls `execute.run()`, which performs the computation and writes results to `data.json` (including runtime in seconds). A `.done` marker is written on completion.

```bash
poetry run python worker.py <root_dir>
```

Multiple workers can be launched in parallel:

```bash
poetry run python worker.py my-run &
poetry run python worker.py my-run &
poetry run python worker.py my-run &
wait
```

### 3. Aggregate (`aggregate.py`)

Reads all `data.json` files from partition subdirectories, combines the results, and produces interactive Plotly visualizations.

```bash
poetry run python aggregate.py <root_dir>
```

### Quick Run

`run-example-local.sh` runs all three stages sequentially:

```bash
./run-example-local.sh my-run --max-n 5000 --partition-size 500
```

## Example: Sieve of Eratosthenes

The included example finds prime numbers using a segmented Sieve of Eratosthenes and visualizes the results.

- **Distribute**: Partitions the range `[2, max_n]` into fixed-size intervals
- **Execute**: Finds all primes in each partition's interval
- **Aggregate**: Produces an [Ulam spiral](https://en.wikipedia.org/wiki/Ulam_spiral) and a prime counting function plot

### Segmented Sieve of Eratosthenes

The classic Sieve of Eratosthenes finds all primes up to *N* by maintaining a boolean array and marking multiples of each prime as composite. The segmented variant (`sieve_range` in `execute.py`) adapts this to find primes in an arbitrary range `[start, end]` without needing an array of size *N*:

1. **Small primes**: Run a standard sieve up to `floor(sqrt(end))` to find all small primes. Any composite number in `[start, end]` must have a factor no larger than `sqrt(end)`, so these small primes are sufficient.

2. **Segment sieve**: Allocate a boolean array of size `end - start + 1` (the segment). For each small prime *p*, compute the first multiple of *p* that falls within `[start, end]`, then mark all multiples of *p* in the segment as composite. Care is taken not to mark *p* itself as composite.

3. **Collect**: All indices still marked `True` correspond to primes.

This approach uses O(end - start) memory rather than O(end), making it suitable for partitioned parallel execution where each worker handles a different segment of the number line.

## Key Dependencies

- **plotly**: Interactive visualization
- Python >=3.10, managed with Poetry
