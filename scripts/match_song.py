import boto3, json, os, sys, random
from botocore.config import Config

s3 = boto3.client(
    's3',
    endpoint_url=f"https://{os.getenv('CF_ACCOUNT_ID')}.r2.cloudflarestorage.com",
    aws_access_key_id=os.getenv('R2_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('R2_SECRET_KEY'),
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

BUCKET = os.getenv('R2_BUCKET', 'instagram-videos')
MOOD_MAP = {
    'calm':          ['lofi', 'ambient', 'soft'],
    'energetic':     ['upbeat', 'hiphop', 'pop'],
    'inspirational': ['motivational', 'cinematic', 'epic'],
    'sunset':        ['lofi', 'chill', 'acoustic'],
    'nature':        ['ambient', 'acoustic', 'calm'],
}

def match_song(video_mood):
    preferred_tags = MOOD_MAP.get(video_mood, ['lofi', 'ambient'])

    response = s3.list_objects_v2(Bucket=BUCKET, Prefix='songs/')
    all_songs = [obj['Key'] for obj in response.get('Contents', [])
                 if obj['Key'].endswith('.mp3')]

    # Try to match by tag in filename
    matched = []
    for song in all_songs:
        song_name = song.lower()
        if any(tag in song_name for tag in preferred_tags):
            matched.append(song)

    chosen = random.choice(matched if matched else all_songs)
    filename = chosen.split('/')[-1]

    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET, 'Key': chosen},
        ExpiresIn=3600
    )

    result = {'filename': filename, 'key': chosen, 'download_url': url}
    print(json.dumps(result))

mood = sys.argv[1] if len(sys.argv) > 1 else 'inspirational'
match_song(mood)
