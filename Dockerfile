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

COPY scripts/ /home/node/scripts/

RUN chmod +x /home/node/scripts/*.py

USER node

EXPOSE 5678

CMD ["n8n", "start"]
