import sys
import pickle
import datetime
from utils import get_json, set_json, precision, mean_precision, upload_file

def get_k_similar(model, target, k):
    indices, distances = model.similar_items(target-1, N=5, filter_items=[target-1])
    return [x+1 for x in indices]
def evaluate(bucket, name):
    validation = pickle.load(open('data/actual/scrobbles.pkl', 'rb'))
    model = pickle.load(open(f"models/{name}.pkl", 'rb'))
    models = get_json(bucket, 'models.json')
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
    now = datetime.now().strftime('%m.%d.%Y_%H:%M:%S')
    models['models'].append({
        "name":name,
        "score":score,
        "date":now
    })
    upload_file(bucket, f"models/{name}.pkl", f"models/{name}.pkl")
    set_json(models, bucket, 'models.json')

if __name__ == "__main__":
    evaluate(sys.argv[1], sys.argv[2])