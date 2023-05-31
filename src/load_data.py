import os
import sys
import pickle
from utils import get_json, get_pickle

def download_scrobbles(config, bucket):
    pickle.dump(get_pickle(bucket, f"data/{config['LastModified']}/scrobbles.pkl"), open('data/actual/scrobbles.pkl', 'wb'))
    pickle.dump(get_pickle(bucket, f"data/{config['LastModified']}/scrobbles_sparse_normalized.pkl"), open('data/actual/scrobbles_sparse_normalized.pkl', 'wb'))
def load_data(bucket):
    config = get_json(bucket, 'config.json')
    os.makedirs(f"data/actual/", exist_ok=True)
    download_scrobbles(config, bucket)

if __name__ == "__main__":
    load_data(sys.argv[1])