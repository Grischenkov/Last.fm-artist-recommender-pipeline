import os
import sys
import pickle
import numpy as np
from utils import get_json, get_csv, upload_file
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

def process_scrobbles(config, bucket):
    scrobbles = get_csv(bucket, 'data/raw/lastfm_user_scrobbles.csv')
    scrobbles.drop_duplicates(['user_id', 'artist_id'], inplace=True)
    users_indexes, users_positions = np.unique(scrobbles.values[:,0], return_inverse=True)
    artists_indexes, artists_positions = np.unique(scrobbles.values[:,1], return_inverse=True)
    scrobbles_sparse = csr_matrix((scrobbles.values[:,2], (users_positions, artists_positions)))
    scrobbles_sparse_normalized = normalize(scrobbles_sparse, norm='l2', axis=1)
    pickle.dump(scrobbles.groupby('user_id')['artist_id'].apply(list).to_dict(), open(f"data/{config['LastModified']}/scrobbles.pkl", 'wb'))
    pickle.dump(scrobbles_sparse_normalized, open(f"data/{config['LastModified']}/scrobbles_sparse_normalized.pkl", 'wb'))
    upload_file(bucket, f"data/{config['LastModified']}/scrobbles.pkl", f"data/{config['LastModified']}/scrobbles.pkl")
    upload_file(bucket, f"data/{config['LastModified']}/scrobbles_sparse_normalized.pkl", f"data/{config['LastModified']}/scrobbles_sparse_normalized.pkl")
def process_data(bucket):
    config = get_json(bucket, 'config.json')
    if config['IsActual'] == False:
        os.makedirs(f"data/{config['LastModified']}/", exist_ok=True)
        process_scrobbles(config, bucket)

if __name__ == "__main__":
    process_data(sys.argv[1])
