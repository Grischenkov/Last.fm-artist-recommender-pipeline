import sys
from utils import get_json, set_json

def select_best_model(bucket):
    config = get_json(bucket, 'config.json')
    models = get_json(bucket, 'models.json')
    best_score = 0
    best_model = ''
    for model in models['models']:
        if model['date'] > config['LastModified']:
            if model['score'] > best_score:
                best_score = model['score']
                best_model = model['name']
    config['ActualModel'] = best_model
    config['ActualScore'] = best_score
    config['IsActual'] = True
    set_json(config, bucket, 'config.json')

if __name__ == "__main__":
    select_best_model(sys.argv[1])