#!/usr/bin/env python3
import json
import math
import time
from pathlib import Path


def sieve_range(start, end):
    """Find primes in [start, end] using a segmented Sieve of Eratosthenes."""
    if end < 2:
        return []
    start = max(start, 2)

    # Find small primes up to sqrt(end)
    limit = int(math.isqrt(end)) + 1
    is_prime_small = [True] * (limit + 1)
    is_prime_small[0] = is_prime_small[1] = False
    for i in range(2, limit + 1):
        if is_prime_small[i]:
            for j in range(i * i, limit + 1, i):
                is_prime_small[j] = False
    small_primes = [i for i in range(2, limit + 1) if is_prime_small[i]]

    # Segmented sieve for [start, end]
    size = end - start + 1
    is_prime = [True] * size

    for p in small_primes:
        # Find first multiple of p >= start
        first = ((start + p - 1) // p) * p
        if first == p:
            first += p  # Don't mark p itself
        for j in range(first, end + 1, p):
            is_prime[j - start] = False

    return [start + i for i in range(size) if is_prime[i]]


def run(work_dir):
    with open(work_dir / "config.json", "r") as f:
        config = json.load(f)

    start = config["start"]
    end = config["end"]

    t0 = time.perf_counter()
    primes = sieve_range(start, end)
    runtime = time.perf_counter() - t0

    with open(work_dir / "data.json", "w") as f:
        json.dump({"primes": primes, "runtime": runtime}, f)

    print(f"Running execute.run on {work_dir.name}: found {len(primes)} primes in [{start}, {end}] ({runtime:.4f}s)")
