import hashlib
import json

import boto3
import botocore

S3_URL_FORMAT = "https://{bucket}.s3.{region}.amazonaws.com/{key}"
S3_URI_FORMAT = "s3://{bucket}/{key}"

s3 = boto3.resource("s3")

def get_or_create_bucket(name):
    """Gets an S3 bucket with boto3 or creates it if it doesn't exist."""
    try: # try to create a bucket
        name, response = _create_bucket(name)
    except botocore.exceptions.ClientError as err:
        # error handling from https://github.com/boto/boto3/issues/1195#issuecomment-495842252
        status = err.response["ResponseMetadata"]["HTTPStatusCode"] # status codes identify particular errors

        if status == 409:  # if the bucket exists already,
            pass # we don't need to make it -- we presume we have the right permissions
        else:
            raise err 
    
    bucket = s3.Bucket(name)

    return bucket

def _create_bucket(name):
    """Creates a bucket with the provided name."""
    session = boto3.session.session() # sessions hold on to credentials and config
    current_region = session.region_name # so we can pull the default region
    bucket_config = {"LocationConstraint": current_region} # and apply it to the bucket

    bucket_reponse = s3.create_bucket(Bucket=name, CreateBucketConfiguration=bucket_config)

    return name, bucket_reponse

def _format_url(bucket_name, region, key=None):
    key = key or ""
    url = S3_URL_FORMAT.format(bucket=bucket_name, region=region, key=key)
    return url

def _format_uri(bucket_name, key=None):
    key = key or ""
    uri = S3_URI_FORMAT.format(bucket=bucket_name, key=key)
    return uri




