# Installation Guide

## Prerequisites

- Python 3.10+ with `venv`
- GCC toolchain (for the `core-os` demo)

## Local Setup

```bash
./scripts/bootstrap.sh
```

The bootstrap script creates `.venv`. No external Python dependencies are required.

## Optional: Clean Reset

```bash
rm -rf .venv outputs models data/radio_frequencies.csv
```

Then rerun the bootstrap and quickstart commands.
