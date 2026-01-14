from rf_research.config import RFConfig
from rf_research.evaluation import evaluate_model, save_evaluation_report


if __name__ == "__main__":
    config = RFConfig()
    report = evaluate_model(config)
    save_evaluation_report(report, config.report_path)
    print("Evaluation complete. Report written to", config.report_path)
