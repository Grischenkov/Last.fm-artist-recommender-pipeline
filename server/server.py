import os
import json
import boto3
import pickle
import pandas as pd

from flask import Flask, request, render_template

app = Flask(__name__)

bucket = 'LastFM-artist-recommender'

s3 = boto3.client(
    service_name='s3',
    endpoint_url='https://s3.storage.selcloud.ru',
    aws_access_key_id='236346_docker',
    aws_secret_access_key='112y;8U\K<Sh'
)

def load_server():
    config = json.load(s3.get_object(Bucket=bucket, Key=f"config.json")['Body'])
    model = pickle.load(s3.get_object(Bucket=bucket, Key=f"models/{config['ActualModel']}.pkl")['Body'])
    data = pd.read_csv(s3.get_object(Bucket=bucket, Key=f"data/raw/lastfm_artist_list.csv")['Body'])["artist_name"].to_dict()
    return (model, data)
model, data = load_server()

def __get_id_by_name(artists_dict, name: str) -> int:
    return next((i for i, n in artists_dict.items() if n == name), None)
def __get_names_from_indexes(artists_dict, indexes: list) -> list:
    return [artists_dict[i] for i in indexes]

@app.route('/update', methods=['POST'])
def update():
    global model
    global data
    model, data = load_server()
@app.route('/')
def pag():
    update()
    return render_template('index.html')
@app.route('/', methods=['POST'])
def page():
    try:
        target = int(__get_id_by_name(data, request.form['text'].strip().lstrip()))
        indices, distances = model.similar_items(target-1, N=5, filter_items=[target-1])
        return __get_names_from_indexes(data, [x+1 for x in indices])
    except:
        return "err"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)