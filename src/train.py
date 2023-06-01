import os
import sys
import pickle
import implicit
from datetime import datetime
from utils import get_json, set_json, get_pickle, upload_file

def get_max_id(models):
    id = 0
    for model in models['models']:
        for i in model:
            if i['id'] > id:
                id = model['id']
    return id
def train(bucket, name):
    config = get_json(bucket, 'config.json')
    models = get_json(bucket, 'models.json')
    
    os.makedirs(f"data/actual/", exist_ok=True)
    os.makedirs(f"models/", exist_ok=True)
    pickle.dump(get_pickle(bucket, f"data/{config['LastModified']}/scrobbles_sparse_normalized.pkl"), open('data/actual/scrobbles_sparse_normalized.pkl', 'wb'))
    
    model = eval(name)
    model.fit(pickle.load(open('data/actual/scrobbles_sparse_normalized.pkl', 'rb')))

    now = datetime.now().strftime('%m.%d.%Y_%H:%M:%S')

    pickle.dump(model, open(f"models/{name}_{now}.pkl", 'wb'))
    upload_file(bucket, f"models/{name}_{now}.pkl", f"models/{name}_{now}.pkl")

    models['models'].append({
            "name":f"{name}_{now}",
            "score":0,
            "date":now
        }
    )
    set_json(models, bucket, 'models.json')
    
    config['IsActual'] = False
    set_json(config, bucket, 'config.json')

if __name__ == "__main__":
    train(sys.argv[1], sys.argv[2])
