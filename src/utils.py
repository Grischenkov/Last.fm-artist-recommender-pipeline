import os
import json
import boto3
import pickle
import numpy as np
import pandas as pd

def precision(actual, predicted):
    return len(list(set(actual) & set(predicted))) / len(predicted)

def mean_precision(scores, n):
    return np.array(scores).sum() / n

def download_file(bucket, filename):
    s3 = boto3.client(
        service_name='s3',
        endpoint_url='https://s3.storage.selcloud.ru'
    )
    return s3.get_object(Bucket=bucket, Key=filename)

def upload_file(bucket, filename, filepath):
    s3 = boto3.client(
        service_name='s3',
        endpoint_url='https://s3.storage.selcloud.ru'
    )
    s3.upload_file(filename, bucket, filepath)

def get_file_last_update_date(bucket, filename):
    s3 = boto3.client(
        service_name='s3',
        endpoint_url='https://s3.storage.selcloud.ru'
    )
    return s3.get_object(Bucket=bucket, Key=filename)['LastModified']

def get_json(bucket, name):
    return json.load(download_file(bucket, name)['Body'])

def set_json(data, bucket, name):
    with open(name, 'w') as file:
        json.dump(data, file)
    upload_file(bucket, name, name)
    os.remove(name)

def get_csv(bucket, filename):
    return pd.read_csv(download_file(bucket, filename)['Body'])

def get_pickle(bucket, filename):
    return pickle.load(download_file(bucket, filename)['Body'])