# Contributing to RF Research Toolkit

Thanks for helping improve this project! This repo is designed to be runnable locally, so contributions should keep the workflows deterministic and self-contained.

## Development Workflow

1. Fork and clone the repository.
2. Create a feature branch.
3. Run verification before opening a PR:

```bash
./scripts/verify.sh
```

## Coding Guidelines

- Prefer deterministic behavior for data generation and tests.
- Keep dependencies minimal and pinned in `requirements.txt`.
- Update documentation when behavior changes.
- Add tests for new functionality.

## Reporting Issues

When filing a bug report, include:

- OS and Python version
- Exact command(s) run
- Console output or stack trace

## Code of Conduct

By participating, you agree to follow the Contributor Covenant Code of Conduct (v2.0).
