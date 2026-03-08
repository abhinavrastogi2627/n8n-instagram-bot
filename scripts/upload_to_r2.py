import boto3, sys, json, os
from botocore.config import Config
from datetime import datetime

s3 = boto3.client(
    's3',
    endpoint_url=f"https://{os.getenv('CF_ACCOUNT_ID')}.r2.cloudflarestorage.com",
    aws_access_key_id=os.getenv('R2_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('R2_SECRET_KEY'),
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

BUCKET      = os.getenv('R2_BUCKET', 'instagram-videos')
PUBLIC_URL  = os.getenv('R2_PUBLIC_URL')  # https://pub-XXXXX.r2.dev

def upload(local_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    key = f"processed/reel_{timestamp}.mp4"

    s3.upload_file(
        local_path, BUCKET, key,
        ExtraArgs={'ContentType': 'video/mp4'}
    )

    public_url = f"{PUBLIC_URL}/{key}"
    print(json.dumps({'public_url': public_url, 'key': key}))

upload(sys.argv[1])
