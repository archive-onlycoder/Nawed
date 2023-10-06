from google.cloud import storage
from trash.config import (
    GCS_S3_BUCKET_NAME,
    GCS_CREDENTIALS_PATH
)
from PIL import Image
import io

def _get_gcs_public_url(bucket_name: str, object_name: str, secure: bool=True):
    scheme = "https" if secure else "http"
    return f"{scheme}://storage.googleapis.com/{bucket_name}/{object_name}"



def _upload_to_gcs(bucket_name: str, file_name: str, buffer: bytes):
    client = storage.Client.from_service_account_json(GCS_CREDENTIALS_PATH)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(buffer)

    return _get_gcs_public_url(bucket_name, file_name)


def rtn_url(image_path):
    image = Image.open(image_path)

    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        
    print(_upload_to_gcs(GCS_S3_BUCKET_NAME, 'test.png', buffer.getvalue()))