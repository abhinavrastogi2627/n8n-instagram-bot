import subprocess, sys, json, os, tempfile, urllib.request

def download(url, suffix):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    urllib.request.urlretrieve(url, tmp.name)
    return tmp.name

def compose(video_url, song_url, quote, output_path):
    # Download files to temp
    video_path = download(video_url, '.mp4')
    song_path  = download(song_url, '.mp3')

    # Clean quote for FFmpeg (escape special chars)
    quote_clean = quote.replace("'", "\\'").replace(":", "\\:")

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", song_path,
        "-filter_complex",
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"drawtext=text='{quote_clean}':"
        f"fontsize=52:"
        f"fontcolor=white:"
        f"x=(w-text_w)/2:"
        f"y=h-th-120:"
        f"shadowcolor=black@0.8:"
        f"shadowx=3:shadowy=3:"
        f"box=1:boxcolor=black@0.3:boxborderw=20[v];"
        f"[1:a]volume=0.7[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        "-shortest",
        "-t", "30",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Cleanup temp files
    os.unlink(video_path)
    os.unlink(song_path)

    if result.returncode != 0:
        print(json.dumps({"error": result.stderr}))
        sys.exit(1)

    print(json.dumps({"output_path": output_path, "success": True}))

params = json.loads(sys.argv[1])
compose(
    params['video_url'],
    params['song_url'],
    params['quote'],
    params.get('output_path', '/tmp/reel_output.mp4')
)
