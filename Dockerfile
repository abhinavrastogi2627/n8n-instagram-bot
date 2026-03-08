FROM node:18-alpine

# Install system packages
RUN apk add --no-cache \
    ffmpeg \
    python3 \
    py3-pip \
    curl \
    fontconfig \
    ttf-dejavu-sans

# Install n8n
RUN npm install -g n8n

# Install Python packages
RUN pip3 install boto3 requests --break-system-packages

# Copy scripts
COPY scripts/ /home/node/scripts/
RUN chmod +x /home/node/scripts/*.py

EXPOSE 5678

CMD ["n8n", "start"]
