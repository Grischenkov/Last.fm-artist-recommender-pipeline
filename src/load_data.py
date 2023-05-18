import sys
import boto3
import pandas as pd


def process_csv(bucket, filename):
    s3 = boto3.client(
        service_name='s3',
        endpoint_url='https://s3.storage.selcloud.ru'
    )
    pd.read_csv(s3.get_object(Bucket=bucket, Key=filename)['Body']).to_csv(filename)

if __name__ == "__main__":
    process_csv(sys.argv[1], sys.argv[2])