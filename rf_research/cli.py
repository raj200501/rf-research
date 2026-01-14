"""Command-line entrypoint for RF research workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rf_research.config import RFConfig
from rf_research.data import generate_synthetic_dataset, write_dataset_csv
from rf_research.distributed.hadoop_job import aggregate_signal_strength
from rf_research.distributed.spark_job import process_data
from rf_research.evaluation import evaluate_model, save_evaluation_report
from rf_research.national_security.analysis import analyze_and_save
from rf_research.national_security.collection import collect_and_save
from rf_research.pipeline import run_pipeline
from rf_research.training import save_training_report, train_and_save


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--data", type=Path, help="Path to the RF dataset CSV")
    parser.add_argument("--model", type=Path, help="Path to the model artifact")
    parser.add_argument("--outputs", type=Path, help="Directory for outputs")


def _config_from_args(args: argparse.Namespace) -> RFConfig:
    config = RFConfig()
    if args.data:
        config = config.__class__(**{**config.__dict__, "data_path": args.data})
    if args.model:
        config = config.__class__(**{**config.__dict__, "model_path": args.model})
    if args.outputs:
        outputs = args.outputs
        config = config.__class__(
            **{
                **config.__dict__,
                "processed_path": outputs / "processed_radio_frequencies.csv",
                "report_path": outputs / "evaluation_report.json",
                "collection_path": outputs / "rf_collection.json",
                "analysis_path": outputs / "rf_analysis.json",
            }
        )
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description="RF Research CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate synthetic dataset")
    _add_common_args(generate_parser)

    train_parser = subparsers.add_parser("train", help="Train the ML model")
    _add_common_args(train_parser)

    eval_parser = subparsers.add_parser("evaluate", help="Evaluate the ML model")
    _add_common_args(eval_parser)

    spark_parser = subparsers.add_parser("spark", help="Run Spark-style processing")
    _add_common_args(spark_parser)

    hadoop_parser = subparsers.add_parser("hadoop", help="Run Hadoop-style processing")
    _add_common_args(hadoop_parser)

    collect_parser = subparsers.add_parser("collect", help="Collect RF data")
    _add_common_args(collect_parser)

    analyze_parser = subparsers.add_parser("analyze", help="Analyze RF data")
    _add_common_args(analyze_parser)

    pipeline_parser = subparsers.add_parser("pipeline", help="Run full pipeline")
    _add_common_args(pipeline_parser)

    args = parser.parse_args()
    config = _config_from_args(args)
    config.ensure_directories()

    if args.command == "generate":
        dataset = generate_synthetic_dataset(config)
        write_dataset_csv(config.data_path, dataset)
        print(json.dumps({"data_path": str(config.data_path)}, indent=2))
        return 0
    if args.command == "train":
        report = train_and_save(config)
        save_training_report(report, config.report_path)
        print(json.dumps(report, indent=2))
        return 0
    if args.command == "evaluate":
        report = evaluate_model(config)
        save_evaluation_report(report, config.report_path)
        print(json.dumps(report, indent=2))
        return 0
    if args.command == "spark":
        output = process_data(config)
        print(json.dumps({"processed_path": str(output)}, indent=2))
        return 0
    if args.command == "hadoop":
        output = aggregate_signal_strength(config)
        print(json.dumps({"summary_path": str(output)}, indent=2))
        return 0
    if args.command == "collect":
        output = collect_and_save(config)
        print(json.dumps({"collection_path": str(output)}, indent=2))
        return 0
    if args.command == "analyze":
        output = analyze_and_save(config)
        print(json.dumps({"analysis_path": str(output)}, indent=2))
        return 0
    if args.command == "pipeline":
        result = run_pipeline(config)
        print(json.dumps(result.__dict__, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
