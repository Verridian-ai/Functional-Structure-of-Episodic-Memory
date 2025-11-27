# Deployment Guide

Guide for deploying Verridian AI to production environments.

## Overview

Deployment options:
1. **Docker** - Containerized deployment
2. **Vercel** - Frontend hosting
3. **Cloud VMs** - AWS, GCP, Azure
4. **Local Server** - On-premises deployment

---

## Docker Deployment

### Dockerfile (Backend)

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ src/
COPY gsw_pipeline.py .
COPY run_full_system.py .

# Environment
ENV PYTHONUNBUFFERED=1

# Expose port (if running API server)
EXPOSE 8000

CMD ["python", "gsw_pipeline.py"]
```

### Dockerfile (Frontend)

```dockerfile
# ui/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

# Build
RUN npm run build

# Expose port
EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - MEM0_API_KEY=${MEM0_API_KEY}
    volumes:
      - ./data:/app/data

  frontend:
    build:
      context: ./ui
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    depends_on:
      - backend
```

### Deploy with Docker

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Vercel Deployment (Frontend)

### 1. Connect Repository

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Select the `ui` directory as root

### 2. Configure Build

```json
// vercel.json
{
    "buildCommand": "npm run build",
    "outputDirectory": ".next",
    "framework": "nextjs",
    "installCommand": "npm install"
}
```

### 3. Environment Variables

Add in Vercel dashboard:
- `OPENROUTER_API_KEY` (optional - usually passed from client)
- `MEM0_API_KEY` (if using server-side memory)

### 4. Deploy

```bash
# Using Vercel CLI
npm i -g vercel
cd ui
vercel
```

---

## Cloud VM Deployment

### AWS EC2

1. Launch EC2 instance (t3.medium or larger)
2. Install dependencies:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.10 python3.10-venv python3-pip -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Clone repo
git clone https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory.git
cd Functional-Structure-of-Episodic-Memory

# Setup backend
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ui && npm install && npm run build
```

3. Configure systemd service:

```ini
# /etc/systemd/system/verridian.service
[Unit]
Description=Verridian AI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Functional-Structure-of-Episodic-Memory
Environment="OPENROUTER_API_KEY=sk-or-..."
ExecStart=/home/ubuntu/Functional-Structure-of-Episodic-Memory/venv/bin/python gsw_pipeline.py
Restart=always

[Install]
WantedBy=multi-user.target
```

4. Start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable verridian
sudo systemctl start verridian
```

### GCP Compute Engine

Similar to AWS EC2, use a `e2-medium` or larger instance.

### Azure VM

Similar to AWS EC2, use a `Standard_B2s` or larger instance.

---

## Environment Configuration

### Production Environment Variables

```bash
# Required
OPENROUTER_API_KEY=sk-or-production-key

# Optional
MEM0_API_KEY=m0-production-key
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1

# Observability (optional)
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://langfuse.example.com
```

### Secrets Management

**AWS Secrets Manager:**
```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])
```

**Environment Files:**
```bash
# Never commit .env to git
# Use .env.production for production values
cp .env.example .env.production
```

---

## Reverse Proxy (Nginx)

### Configuration

```nginx
# /etc/nginx/sites-available/verridian
server {
    listen 80;
    server_name verridian.example.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name verridian.example.com;

    ssl_certificate /etc/letsencrypt/live/verridian.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/verridian.example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # SSE support for streaming
    location /api/chat {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        chunked_transfer_encoding off;
    }
}
```

### SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d verridian.example.com
```

---

## Monitoring

### Health Checks

Add health endpoint:

```typescript
// ui/src/app/api/health/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
    return NextResponse.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: process.env.npm_package_version
    });
}
```

### Logging

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/verridian/app.log')
    ]
)
```

### LangFuse Observability

```python
from src.observability.langfuse_tracer import trace, get_tracer

tracer = get_tracer()

@trace(name="process_query")
def process_query(query: str):
    # Processing...
    pass
```

---

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.scale.yml
services:
  frontend:
    deploy:
      replicas: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### Load Balancing

```nginx
upstream frontend {
    server frontend1:3000;
    server frontend2:3000;
    server frontend3:3000;
}

server {
    location / {
        proxy_pass http://frontend;
    }
}
```

---

## Backup and Recovery

### Workspace Backups

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d)
tar -czf backup_${DATE}.tar.gz data/workspaces/
aws s3 cp backup_${DATE}.tar.gz s3://verridian-backups/
```

### Cron Schedule

```bash
# Daily backup at 2 AM
0 2 * * * /home/ubuntu/Functional-Structure-of-Episodic-Memory/backup.sh
```

---

## Security Checklist

- [ ] HTTPS enabled with valid certificates
- [ ] API keys stored in secrets manager
- [ ] Firewall configured (only 80/443 open)
- [ ] Regular security updates
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] CORS properly configured
- [ ] No sensitive data in logs

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
lsof -i :3000
kill -9 <PID>
```

**Permission denied:**
```bash
sudo chown -R $USER:$USER /app/data
```

**Out of memory:**
- Increase swap space
- Use smaller model
- Implement request queuing

**SSL certificate errors:**
```bash
sudo certbot renew --dry-run
```

---

## Related Pages

- [Quick-Start](Quick-Start) - Getting started
- [Development-Guide](Development-Guide) - Development setup
- [Architecture-Overview](Architecture-Overview) - System design
