# Usage Guide

## Run the Full Workflow

```bash
./scripts/run.sh
```

## Machine Learning Models

Train the model and produce a report:

```bash
python -m rf_research.cli train
```

Evaluate the model:

```bash
python -m rf_research.cli evaluate
```

## Distributed Systems (Local Simulation)

Spark-like data processing:

```bash
python -m rf_research.cli spark
```

Hadoop-like aggregation:

```bash
python -m rf_research.cli hadoop
```

## Core OS Demo

```bash
make -C core-os
./core-os/ai_integration secure
./core-os/ai_integration monitor 2 1
```

## National Security Simulation

Collect RF data locally:

```bash
python -m rf_research.cli collect
```

Analyze the collection:

```bash
python -m rf_research.cli analyze
```
