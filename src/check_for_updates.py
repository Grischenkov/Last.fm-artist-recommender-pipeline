import sys
from utils import get_json, set_json, get_file_last_update_date

def check_for_updates(bucket):
    config = get_json(bucket, 'config.json')
    last_update_date = max([
            get_file_last_update_date(bucket, 'data/raw/lastfm_artist_list.csv'), 
            get_file_last_update_date(bucket, 'data/raw/lastfm_user_scrobbles.csv')
        ]
    ).strftime('%m.%d.%Y_%H:%M:%S')
    if config['LastModified'] != last_update_date:
        config['LastModified'] = last_update_date
        config['IsActual'] = False
        set_json(config, bucket, 'config.json')

if __name__ == "__main__":
    check_for_updates(sys.argv[1])