FROM n8nio/n8n:latest

USER root

# n8n now uses a Debian-based image, use apt-get instead of apk
RUN apt-get update && apt-get install -y \
    ffmpeg \
    python3 \
    python3-pip \
    curl \
    fontconfig \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install boto3 requests --break-system-packages

COPY scripts/ /home/node/scripts/

RUN chmod +x /home/node/scripts/*.py

USER node

EXPOSE 5678

CMD ["n8n", "start"]
