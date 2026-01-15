from rf_research.config import RFConfig
from rf_research.training import save_training_report, train_and_save


if __name__ == "__main__":
    config = RFConfig()
    report = train_and_save(config)
    save_training_report(report, config.report_path)
    print("Training complete. Report written to", config.report_path)
