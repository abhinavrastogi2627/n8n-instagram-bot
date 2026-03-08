import boto3, json, os, random
from datetime import datetime, timedelta
from botocore.config import Config

# R2 credentials from environment
s3 = boto3.client(
    's3',
    endpoint_url=f"https://{os.getenv('CF_ACCOUNT_ID')}.r2.cloudflarestorage.com",
    aws_access_key_id=os.getenv('R2_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('R2_SECRET_KEY'),
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

BUCKET = os.getenv('R2_BUCKET', 'instagram-videos')

def get_posted_log():
    try:
        obj = s3.get_object(Bucket=BUCKET, Key='posted-log.json')
        return json.loads(obj['Body'].read())
    except:
        return []

def pick_video():
    posted = get_posted_log()
    recent = [p['filename'] for p in posted
              if datetime.fromisoformat(p['date']) > datetime.now() - timedelta(days=30)]

    # List videos in raw-videos/ folder
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix='raw-videos/')
    all_videos = [obj['Key'] for obj in response.get('Contents', [])
                  if obj['Key'].endswith(('.mp4', '.mov'))]

    # Filter out recently posted
    available = [v for v in all_videos if v.split('/')[-1] not in recent]

    if not available:
        available = all_videos  # Reset if all posted

    chosen = random.choice(available)
    filename = chosen.split('/')[-1]

    # Generate presigned URL for download
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET, 'Key': chosen},
        ExpiresIn=3600
    )

    # Infer mood from filename tags (e.g., "sunset_calm_beach.mp4")
    tags = filename.replace('.mp4','').replace('.mov','').split('_')
    mood = tags[1] if len(tags) > 1 else 'inspirational'

    result = {
        'filename': filename,
        'key': chosen,
        'download_url': url,
        'mood': mood,
        'tags': tags
    }
    print(json.dumps(result))

pick_video()
