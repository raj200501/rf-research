from rf_research.config import RFConfig
from rf_research.distributed.hadoop_job import aggregate_signal_strength


if __name__ == "__main__":
    config = RFConfig()
    output = aggregate_signal_strength(config)
    print("Summary written to", output)
