from rf_research.config import RFConfig
from rf_research.national_security.analysis import analyze_and_save


if __name__ == "__main__":
    config = RFConfig()
    output = analyze_and_save(config)
    print("Analysis report written to", output)
