FROM n8nio/n8n:latest

USER root

# Install FFmpeg and Python
RUN apk add --no-cache \
    ffmpeg \
    python3 \
    py3-pip \
    py3-requests \
    curl

# Install Python dependencies
RUN pip3 install requests python-dotenv --break-system-packages

USER node

# Verify FFmpeg installed
RUN ffmpeg -version

EXPOSE 5678
CMD ["n8n", "start"]
