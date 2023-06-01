import sys
from utils import get_json, set_json

def validate_storage(bucket):
    try:
        config = get_json(bucket, 'config.json')
    except:
        config = {
            "LastModified": None, 
            "ActualModel": None, 
            "ActualScore": 0, 
            "IsActual": False
        }
        set_json(config, bucket, 'config.json')
    try:
        models = get_json(bucket, 'models.json')
    except:
        models = {
            "models":[
            ]
        }
        set_json(models, bucket, 'models.json')

if __name__ == "__main__":
    validate_storage(sys.argv[1])
