from rf_research.config import RFConfig
from rf_research.national_security.collection import collect_and_save


if __name__ == "__main__":
    config = RFConfig()
    output = collect_and_save(config)
    print("Collected RF data written to", output)
