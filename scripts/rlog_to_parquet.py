import os
import pandas as pd

from tools.lib.logreader import LogReader
from dashcam_backup.params import (
    BACKUP_CATALOG_FP,
)


if __name__ == "__main__":
    cat = pd.read_csv(BACKUP_CATALOG_FP)
    rlog = cat[cat["local_path"].str.endswith("rlog")]
    for _, row in rlog.iterrows():
        raw_fp = row["local_path"]
        conv_fp = raw_fp.replace("raw_data", "converted_data").replace("rlog", "rlog.parquet")
        if not os.path.exists(conv_fp):
            os.makedirs(os.path.dirname(conv_fp), exist_ok=True)
            lr = LogReader(raw_fp)
            out = []
            for msg in lr:
                try:
                    dict_msg = msg.to_dict()
                    out.append(dict_msg)
                except UnicodeDecodeError:
                    continue
            df = pd.DataFrame(out)
            df.to_parquet(conv_fp)
