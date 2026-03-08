FROM n8nio/n8n:latest

USER root

RUN apk add --no-cache \
    ffmpeg \
    python3 \
    py3-pip \
    curl \
    fontconfig \
    ttf-dejavu

RUN pip3 install boto3 requests --break-system-packages

# Copy scripts into container
COPY scripts/ /home/node/scripts/
RUN chmod +x /home/node/scripts/*.py

USER node

EXPOSE 5678
CMD ["n8n", "start"]
```

Push to GitHub — Railway will auto-redeploy.

### Step 17 — Add All Secrets to Railway Environment Variables

Go to Railway → Your project → **Variables** → add:
```
CF_ACCOUNT_ID          = your_cloudflare_account_id
R2_ACCESS_KEY          = your_r2_access_key
R2_SECRET_KEY          = your_r2_secret_key
R2_BUCKET              = instagram-videos
R2_PUBLIC_URL          = https://pub-XXXXXXX.r2.dev
META_ACCESS_TOKEN      = EAAxxxxxxxxx
INSTAGRAM_ACCOUNT_ID   = 17841XXXXXXXX
```

---

## PHASE 5 — Build the n8n Workflow

### Step 18 — Open n8n and Create New Workflow

1. Open your Railway n8n URL
2. Click **+ New Workflow**
3. Name it: `Instagram Daily Auto-Post`

### Step 19 — Add Node 1: Schedule Trigger

1. Click **+** → search **Schedule Trigger**
2. Configure:
   - Trigger: `Cron`
   - Expression: `0 9 * * *` (every day 9 AM UTC — adjust for IST: `30 3 * * *`)
3. Save node

### Step 20 — Add Node 2: Pick Video

1. Connect to Schedule Trigger
2. Click **+** → search **Execute Command**
3. Configure:
```
Command: python3 /home/node/scripts/pick_video.py
