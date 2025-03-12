# HomeBridge Deployment Guide

## Production Deployment Guidelines

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- Nginx or Apache
- SSL/TLS certificate
- Domain name
- Linux server (recommended: Ubuntu 20.04 LTS)

### Security Best Practices

#### 1. Environment Variables
- NEVER commit `.env` files to version control
- Use a secure secret key generator for `SESSION_SECRET`
- Rotate API keys regularly
- Use separate API keys for development and production

```bash
# Required Environment Variables
SESSION_SECRET=<strong-random-key>
GEMINI_API_KEY=<your-production-api-key>
DATABASE_URL=postgresql://user:password@localhost:5432/homebridge
FLASK_ENV=production
```

#### 2. Database Security
- Use strong passwords
- Enable SSL connections
- Implement connection pooling
- Regular backups
- Principle of least privilege for database users

#### 3. Application Security
- Enable CSRF protection
- Set secure cookie flags
- Implement rate limiting
- Use HTTPS only
- Enable security headers
- Implement input validation
- Regular dependency updates

### Production Setup

1. **System Updates**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx postgresql
```

2. **Create Production User**
```bash
sudo useradd -m -s /bin/bash homebridge
sudo usermod -aG www-data homebridge
```

3. **Clone and Setup**
```bash
cd /var/www
sudo git clone https://github.com/yourusername/HomeBridge.git
sudo chown -R homebridge:www-data HomeBridge
cd HomeBridge
```

4. **Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

5. **Database Setup**
```bash
sudo -u postgres createuser homebridge
sudo -u postgres createdb homebridge_prod
sudo -u postgres psql -c "ALTER USER homebridge WITH PASSWORD 'strong-password';"
```

6. **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

7. **Systemd Service**
```ini
[Unit]
Description=HomeBridge Gunicorn Service
After=network.target

[Service]
User=homebridge
Group=www-data
WorkingDirectory=/var/www/HomeBridge
Environment="PATH=/var/www/HomeBridge/venv/bin"
Environment="FLASK_ENV=production"
EnvironmentFile=/var/www/HomeBridge/.env
ExecStart=/var/www/HomeBridge/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5003 app:app

[Install]
WantedBy=multi-user.target
```

### Monitoring and Maintenance

1. **Logging**
- Configure application logging
- Set up log rotation
- Monitor error rates
- Use centralized logging (e.g., ELK stack)

2. **Performance Monitoring**
- Set up application performance monitoring (APM)
- Monitor system resources
- Configure alerts for critical metrics
- Regular performance audits

3. **Backup Strategy**
- Daily database backups
- Regular configuration backups
- Automated backup testing
- Off-site backup storage

### CI/CD Pipeline

1. **GitHub Actions Workflow**
```yaml
name: HomeBridge CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: |
        pytest --cov=./ --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v2

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.DEPLOY_HOST }}
        username: ${{ secrets.DEPLOY_USER }}
        key: ${{ secrets.DEPLOY_KEY }}
        script: |
          cd /var/www/HomeBridge
          git pull
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart homebridge
```

### Security Checklist

- [ ] SSL/TLS certificates installed and configured
- [ ] Environment variables secured
- [ ] Database access restricted and encrypted
- [ ] Regular security updates enabled
- [ ] Firewall configured
- [ ] Rate limiting implemented
- [ ] Input validation in place
- [ ] CSRF protection enabled
- [ ] Security headers configured
- [ ] Logging and monitoring set up
- [ ] Backup strategy implemented
- [ ] CI/CD pipeline secured

### Troubleshooting

1. **Common Issues**
- Port conflicts
- Permission errors
- SSL certificate issues
- Database connection problems

2. **Debugging**
- Check application logs
- Verify environment variables
- Test database connectivity
- Validate nginx configuration

3. **Support**
- Create GitHub issues for bugs
- Document known issues
- Maintain FAQ section
- Set up monitoring alerts 