import os
import io
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import pandas as pd


def send_email(subject, body):

    client = boto3.client('ses', region_name='us-east-2')

    response = client.send_email(
        Destination={
            'ToAddresses': ["rupesh.seeth@gmail.com", "aspatel262@gmail.com"]
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject
            },
        },
        Source='pyjobscraper@gmail.com'
    )

    print(response)


def upload_file(bucket, df, filename):

    key = "files/" + filename

    s3_client = boto3.client('s3')
    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

        response = s3_client.put_object(
            Bucket=bucket, Key=key, Body=csv_buffer.getvalue()
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 put_object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 put_object response. Status - {status}")


def read_df(bucket, filename):

    s3_client = boto3.client('s3')
    path = "files/" + filename
    response = s3_client.get_object(Bucket=bucket, Key=path)

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        df = pd.read_csv(response.get("Body"))
        return df
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")
        return None


def file_exists(bucket, filename):
    s3_client = boto3.client('s3')
    try:
        s3_client.head_object(Bucket=bucket, Key=filename)
        return True
    except ClientError:
        # Not found
        return False


def get_new_postings(curr_postings, prev_postings):

    curr_postings = set(curr_postings[1:-1].split("), "))
    prev_postings = set(prev_postings[1:-1].split("), "))

    return list(curr_postings - prev_postings)
