import os
import pickle as pkl

from tools.lib.logreader import LogReader


if __name__ == "__main__":
    for root, dirs, in os.walk("/media/brian/7ef70690-cfa7-4aea-9ae2-cb402f50dec0/dashcam_backup/raw_data"):
        for d in dirs:
            raw_fp = os.path.join(root, d, "rlog")
            conv_fp = raw_fp.replace("raw_data", "converted_data").replace("rlog", "rlog.pkl")
            if not os.path.exists(conv_fp) and os.path.exists(raw_fp):
                print(raw_fp)
                os.makedirs(os.path.dirname(conv_fp), exist_ok=True)
                lr = LogReader(raw_fp)
                out = []
                for msg in lr:
                    try:
                        dict_msg = msg.to_dict()
                        out.append(dict_msg)
                    except UnicodeDecodeError:
                        continue

                with open(conv_fp, "wb") as f:
                    pkl.dump(out, f)
