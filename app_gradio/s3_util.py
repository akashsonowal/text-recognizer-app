import hashlib
import json

import boto3
import botocore

S3_URL_FORMAT = "https://{bucket}.s3.{region}.amazonaws.com/{key}"
S3_URI_FORMAT = "s3://{bucket}/{key}"

