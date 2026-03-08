import requests, sys, json, os, time

TOKEN      = os.getenv('META_ACCESS_TOKEN')
ACCOUNT_ID = os.getenv('INSTAGRAM_ACCOUNT_ID')

def post_reel(video_url, caption):
    # Step 1: Create container
    print("Creating media container...")
    r = requests.post(
        f"https://graph.facebook.com/v18.0/{ACCOUNT_ID}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": "true",
            "access_token": TOKEN
        }
    )
    data = r.json()
    if 'error' in data:
        print(json.dumps({"error": data['error']['message']}))
        sys.exit(1)

    container_id = data['id']
    print(f"Container ID: {container_id}")

    # Step 2: Poll until ready (max 5 minutes)
    print("Waiting for video processing...")
    for attempt in range(20):
        time.sleep(15)
        status_r = requests.get(
            f"https://graph.facebook.com/v18.0/{container_id}",
            params={"fields": "status_code", "access_token": TOKEN}
        )
        status = status_r.json().get("status_code")
        print(f"Status: {status}")
        if status == "FINISHED":
            break
        elif status == "ERROR":
            print(json.dumps({"error": "Video processing failed on Instagram"}))
            sys.exit(1)

    # Step 3: Publish
    print("Publishing...")
    pub_r = requests.post(
        f"https://graph.facebook.com/v18.0/{ACCOUNT_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": TOKEN
        }
    )
    result = pub_r.json()
    print(json.dumps({"post_id": result.get('id'), "success": True}))

params = json.loads(sys.argv[1])
post_reel(params['video_url'], params['caption'])
