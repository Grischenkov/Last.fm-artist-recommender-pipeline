import os
import sys
from utils import get_json, upload_file

def upload_scrobbles(config, bucket):
    upload_file(bucket, f"data/{config['LastModified']}/scrobbles.pkl", f"data/{config['LastModified']}/scrobbles.pkl")
    os.remove(f"data/{config['LastModified']}/scrobbles.pkl")
    upload_file(bucket, f"data/{config['LastModified']}/scrobbles_sparse_normalized.pkl", f"data/{config['LastModified']}/scrobbles_sparse_normalized.pkl")
    os.remove(f"data/{config['LastModified']}/scrobbles_sparse_normalized.pkl")
def upload_processed_data(bucket):
    config = get_json(bucket, 'config.json')
    if config['IsActual'] == False:
        upload_scrobbles(config, bucket)
        os.rmdir(f"data/{config['LastModified']}")

if __name__ == "__main__":
    upload_processed_data(sys.argv[1])