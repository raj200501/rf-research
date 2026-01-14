# Troubleshooting

## Python or venv issues

If `./scripts/bootstrap.sh` fails:

1. Confirm that Python 3.10+ is installed: `python3 --version`
2. Remove and recreate the virtual environment:

```bash
rm -rf .venv
./scripts/bootstrap.sh
```

## C build issues

If `make -C core-os` fails:

- Verify GCC is available: `gcc --version`
- Ensure the `core-os/include` directory exists (required for `sha256.h`).

## Output files missing

If verification fails due to missing outputs:

1. Remove old artifacts:

```bash
rm -rf outputs models data/radio_frequencies.csv
```

2. Rerun:

```bash
./scripts/verify.sh
```

## Dataset regeneration

The dataset is generated deterministically. If you want a fresh dataset with new randomness, update the `seed` field in `rf_research/config.py` and regenerate.
