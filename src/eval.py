import os
import sys
import pickle
from utils import get_json, set_json, precision, mean_precision, get_pickle


def get_max_id(models):
    id = 0
    for model in models['models']:
        for i in model:
            if i['id'] > id:
                id = model['id']
    return id
def get_k_similar(model, target, k):
    indices, distances = model.similar_items(target-1, N=5, filter_items=[target-1])
    return [x+1 for x in indices]
def evaluate(bucket, name):
    config = get_json(bucket, 'config.json')
    models = get_json(bucket, 'models.json')

    os.makedirs(f"data/actual/", exist_ok=True)
    pickle.dump(get_pickle(bucket, f"data/{config['LastModified']}/scrobbles.pkl"), open('data/actual/scrobbles.pkl', 'wb'))
    validation = pickle.load(open('data/actual/scrobbles.pkl', 'rb'))
    
    id = get_max_id(models)
    name = f"{name}_{id}"

    model = pickle.load(get_pickle(bucket, f"models/{name}.pkl")['Body'])
    
    scores = []
    users = 0
    for user in validation:
        if len(validation[user]) <= 1:
            continue
        predictions = []
        for artist in validation[user]:
            predictions += get_k_similar(model, artist, 5)
        scores.append(precision(validation[user], predictions))
        users += 1
    score = mean_precision(scores, users)

    models['models']['name']['score'] = score
    set_json(models, bucket, 'models.json')

if __name__ == "__main__":
    evaluate(sys.argv[1], sys.argv[2])
