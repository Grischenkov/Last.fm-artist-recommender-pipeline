import sys
import kaggle 
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
    try:
        scrobbles = get_csv(bucket, 'data/raw/lastfm_user_scrobbles.csv')
        artists = get_csv(bucket, 'data/raw/lastfm_artists_list.csv')
    except:
        os.makedirs('data/raw/', exist_ok=True)
        kaggle.api.dataset_download_files('pcbreviglieri/lastfm-music-artist-scrobbles', path='data/raw/', unzip=True)
        upload_file(bucket, 'data/raw/lastfm_user_scrobbles.csv', 'data/raw/lastfm_user_scrobbles.csv')
        upload_file(bucket, 'data/raw/lastfm_artists_list.csv', 'data/raw/lastfm_artists_list.csv')

if __name__ == "__main__":
    validate_storage(sys.argv[1])
