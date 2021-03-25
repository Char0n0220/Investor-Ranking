import logging
import boto3
from botocore.exceptions import ClientError
from utilities.secrets import s3_bucket
from io import StringIO


def upload_to_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
                 file, issuer, currency, object_name=None, json=False):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    folder = currency.upper()

    # If S3 object_name was not specified, use Issuer Name
    if object_name is None:
        object_name = issuer.upper()

    # Prepare the file:
    if json:
        obj_buffer = StringIO()
        file.to_json(obj_buffer)
    else:
        obj_buffer = StringIO()
        file.to_csv(obj_buffer)

    # Upload the file:
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    s3 = session.resource('s3')
    folder_file_name = folder+'/'+object_name
    try:
        response = s3.Object(s3_bucket, folder_file_name).put(Body=obj_buffer.getvalue())
    except ClientError as e:
        logging.error(e)
        return False
    return True
