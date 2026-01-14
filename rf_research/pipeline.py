"""End-to-end pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from rf_research.config import RFConfig
from rf_research.distributed.hadoop_job import aggregate_signal_strength
from rf_research.distributed.spark_job import process_data
from rf_research.evaluation import evaluate_model, save_evaluation_report
from rf_research.national_security.analysis import analyze_and_save
from rf_research.national_security.collection import collect_and_save
from rf_research.training import save_training_report, train_and_save


@dataclass
class PipelineResult:
    training_report: Dict[str, object]
    evaluation_report: Dict[str, object]
    processed_path: str
    summary_path: str
    collection_path: str
    analysis_path: str


def run_pipeline(config: RFConfig) -> PipelineResult:
    config.ensure_directories()
    training_report = train_and_save(config)
    save_training_report(training_report, config.report_path)
    evaluation_report = evaluate_model(config)
    save_evaluation_report(evaluation_report, config.report_path)
    processed_path = process_data(config)
    summary_path = aggregate_signal_strength(config)
    collection_path = collect_and_save(config)
    analysis_path = analyze_and_save(config)
    return PipelineResult(
        training_report=training_report,
        evaluation_report=evaluation_report,
        processed_path=str(processed_path),
        summary_path=str(summary_path),
        collection_path=str(collection_path),
        analysis_path=str(analysis_path),
    )
