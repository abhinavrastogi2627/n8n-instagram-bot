FROM node:18-alpine

RUN apk add --no-cache \
    ffmpeg \
    python3 \
    py3-pip \
    curl

RUN pip3 install boto3 requests --break-system-packages

COPY scripts/ /home/node/scripts/
RUN chmod +x /home/node/scripts/*.py

RUN npm install -g n8n

EXPOSE 5678

CMD ["n8n", "start"]
