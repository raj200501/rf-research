from rf_research.config import RFConfig
from rf_research.distributed.spark_job import process_data


if __name__ == "__main__":
    config = RFConfig()
    output = process_data(config)
    print("Processed data written to", output)
