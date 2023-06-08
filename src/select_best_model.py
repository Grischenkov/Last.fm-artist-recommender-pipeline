import sys
from utils import get_json, set_json

def select_best_model(bucket):
    config = get_json(bucket, 'config.json')
    models = get_json(bucket, 'models.json')
    best_score = config['ActualScore']
    best_model = config['ActualModel']
    for i in range(len(models['models'])):
        if models['models'][i]['date'] > config['LastModified']:
            if models['models'][i]['score'] > best_score:
                best_score = models['models'][i]['score']
                best_model = models['models'][i]['name']
    config['ActualModel'] = best_model
    config['ActualScore'] = best_score
    config['IsActual'] = True
    set_json(config, bucket, 'config.json')

if __name__ == "__main__":
    select_best_model(sys.argv[1])
