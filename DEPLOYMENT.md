# 🚀 Deployment Guide - Corner Chair

This guide covers deploying Corner Chair to production on various platforms.

## Quick Start - Local Development

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/AB00999/corner-chair.git
cd corner-chair/barber-booking-demo

# Create virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
# or
venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Visit http://localhost:5001
```

---

## Heroku Deployment

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed
- Git repository set up

### Step 1: Prepare for Heroku

Create `Procfile` in the `barber-booking-demo` directory:
```
web: gunicorn app:app
```

Add `gunicorn` to `requirements.txt`:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Step 2: Create Heroku App

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set up PostgreSQL (optional, SQLite works on hobby tier)
heroku addons:create heroku-postgresql:hobby-dev
```

### Step 3: Configure Environment

```bash
# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key-here
```

### Step 4: Deploy

```bash
# Push to Heroku
git push heroku main

# Or if deploying from subdirectory
git subtree push --prefix barber-booking-demo heroku main

# View logs
heroku logs --tail
```

### Step 5: Access Your App

```bash
# Open in browser
heroku open

# Your app is now live at: https://your-app-name.herokuapp.com
```

---

## AWS Elastic Beanstalk

### Prerequisites
- AWS account
- AWS CLI installed
- EB CLI installed

### Step 1: Initialize EB Application

```bash
cd barber-booking-demo
eb init -p python-3.9 corner-chair-app
```

### Step 2: Create `.ebextensions/python.config`

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
```

### Step 3: Create Environment and Deploy

```bash
# Create environment
eb create corner-chair-env

# Deploy
eb deploy

# View status
eb status

# Open in browser
eb open
```

---

## DigitalOcean App Platform

### Step 1: Connect GitHub Repository

1. Go to DigitalOcean App Platform
2. Click "Create App"
3. Select your GitHub repository
4. Choose the `barber-booking-demo` directory

### Step 2: Configure App

```yaml
name: corner-chair
services:
  - name: app
    github:
      repo: AB00999/corner-chair
      branch: main
    build_command: pip install -r requirements.txt
    run_command: gunicorn app:app
    http_port: 5001
    envs:
      - key: FLASK_ENV
        value: production
databases:
  - name: db
    engine: sqlite
```

### Step 3: Deploy

Click "Deploy" and DigitalOcean handles the rest.

---

## Docker Containerization

### Step 1: Create Dockerfile

Create `Dockerfile` in `barber-booking-demo`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

### Step 2: Create `.dockerignore`

```
__pycache__
*.pyc
.env
.git
.gitignore
.DS_Store
venv/
tests/
```

### Step 3: Build and Run

```bash
# Build image
docker build -t corner-chair:latest .

# Run container
docker run -p 5001:5000 corner-chair:latest

# Visit http://localhost:5001
```

### Step 4: Deploy to Docker Hub or Container Registry

```bash
# Tag image
docker tag corner-chair:latest yourusername/corner-chair:latest

# Push to Docker Hub
docker push yourusername/corner-chair:latest

# Deploy to Kubernetes, Docker Swarm, etc.
```

---

## Environment Variables

Create `.env` file (development only):

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///cornershop.db
```

**Production variables:**
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=generate-random-key-here
DATABASE_URL=postgresql://user:password@host:port/dbname
```

Generate secret key:
```python
import secrets
print(secrets.token_hex(32))
```

---

## Database Migration (SQLite to PostgreSQL)

### Step 1: Install PostgreSQL Driver

```bash
pip install psycopg2-binary
```

### Step 2: Update Connection String

```python
# app.py
import os
db_url = os.environ.get('DATABASE_URL', 'sqlite:///cornershop.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
```

### Step 3: Migrate Data (if needed)

```bash
# Export from SQLite
sqlite3 cornershop.db ".dump" > backup.sql

# Import to PostgreSQL
psql your_db_name < backup.sql
```

---

## SSL/TLS Configuration

### Using Let's Encrypt (Free)

On Heroku:
```bash
# Automatic with Heroku Paid Dyno
# Or use CloudFlare for free HTTPS
```

On AWS:
```bash
# Use AWS Certificate Manager
# Configure in Load Balancer
```

On DigitalOcean:
```bash
# Automatic free SSL with Let's Encrypt
# Enabled by default
```

---

## Performance Optimization

### 1. Enable Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/services')
@cache.cached(timeout=3600)
def get_services():
    # Cache for 1 hour
    return render_template('services.html')
```

### 2. Database Indexing

```python
# In your models
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, index=True)
    appointment_date = db.Column(db.Date, index=True)
```

### 3. Minify Assets

```bash
pip install flask-minify
```

### 4. CDN for Static Files

```python
# Use CloudFront (AWS) or CloudFlare for static assets
# Configure in production:
STATIC_URL = 'https://cdn.yourdomain.com/static/'
```

---

## Monitoring & Logging

### 1. Application Monitoring

```python
# Use services like:
# - Sentry (error tracking)
# - New Relic (performance)
# - DataDog (infrastructure)

import sentry_sdk
sentry_sdk.init("your-sentry-url")
```

### 2. Log Aggregation

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Use services like:
- ELK Stack
- Splunk
- CloudWatch (AWS)
- Stackdriver (GCP)

---

## Backup & Disaster Recovery

### Automated Backups

```bash
# SQLite backup script
#!/bin/bash
sqlite3 cornershop.db ".backup 'backup-$(date +%Y%m%d).db'"

# PostgreSQL backup
pg_dump your_db_name > backup-$(date +%Y%m%d).sql
```

### Restore from Backup

```bash
# SQLite
sqlite3 cornershop.db < backup.sql

# PostgreSQL
psql your_db_name < backup.sql
```

---

## Testing in Production

### Smoke Tests

```python
# Run basic checks after deployment
import requests

def test_production():
    response = requests.get('https://your-app.herokuapp.com/')
    assert response.status_code == 200
    
    response = requests.get('https://your-app.herokuapp.com/services')
    assert response.status_code == 200
```

### Load Testing

```bash
pip install locust

# Create locustfile.py
# Run load tests
locust -f locustfile.py --host=https://your-app.com
```

---

## Scaling Strategies

### Horizontal Scaling
- Add more application servers
- Use load balancing
- Implement caching layer

### Vertical Scaling
- Increase server resources
- Upgrade database tier
- Use CDN for static files

### Auto-Scaling (AWS/Heroku)
```bash
# Heroku dyno formation
heroku ps:scale web=2 worker=1

# AWS ASG configuration in CloudFormation
```

---

## Security Checklist

Before deploying to production:

- [ ] HTTPS enabled
- [ ] Secret key configured (unique, strong)
- [ ] Database credentials secured
- [ ] CSRF tokens enabled
- [ ] Input validation in place
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (template escaping)
- [ ] Rate limiting enabled
- [ ] Error logging without exposing sensitive info
- [ ] Regular backups configured
- [ ] Security headers configured
- [ ] Dependencies up to date

---

## Rollback Procedures

### Heroku Rollback
```bash
# View releases
heroku releases

# Rollback to previous version
heroku rollback
```

### Git Rollback
```bash
# Revert last commit
git revert HEAD

# Force push (caution!)
git push -f origin main
```

---

## Maintenance

### Regular Tasks
- Monitor application logs
- Review performance metrics
- Update dependencies monthly
- Test backup restoration quarterly
- Review security patches
- Monitor database size
- Check SSL certificate expiration

---

## Troubleshooting

### Common Issues

**App won't start**
```bash
# Check logs
heroku logs --tail

# Check requirements
pip install -r requirements.txt
```

**Database connection error**
```bash
# Verify connection string
heroku config:get DATABASE_URL

# Test connection
python -c "import sqlite3; sqlite3.connect('cornershop.db')"
```

**Static files not loading**
```bash
# Collect static files
python manage.py collectstatic

# Check static file path in app.py
app = Flask(__name__, static_folder='static')
```

---

## Getting Help

- **Heroku**: https://devcenter.heroku.com/
- **AWS**: https://docs.aws.amazon.com/
- **DigitalOcean**: https://docs.digitalocean.com/
- **Flask**: https://flask.palletsprojects.com/
- **GitHub**: https://docs.github.com/

---

**Last Updated:** November 14, 2026  
**Version:** 1.0.0  
**Maintainer:** AB00999

