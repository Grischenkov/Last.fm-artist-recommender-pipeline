import sys
import pickle
from utils import get_json, set_json

def train(bucket, name):
    model = eval(name)
    model.fit(pickle.load(open('data/actual/scrobbles_sparse_normalized.pkl', 'rb')))
    pickle.dump(model, open(f"models/{name}.pkl", 'wb'))
    config = get_json(bucket, 'config.json')
    config['IsActual'] = False
    set_json(config, bucket, 'config.json')

if __name__ == "__main__":
    train(sys.argv[1], sys.argv[2])