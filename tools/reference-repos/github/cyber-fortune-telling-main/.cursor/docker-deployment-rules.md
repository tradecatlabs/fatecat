# Docker & Deployment Rules - Containerized Fortune Telling Application

## Container Architecture

### Service Overview
```yaml
services:
  database:    # PostgreSQL 17.5
  backend:     # Strapi CMS (port 1337)
  frontend:    # Next.js App (port 4000)
```

### Network Configuration
- **Internal Communication**: Services communicate via Docker network
- **External Access**: Frontend exposed on port 4000
- **Database**: PostgreSQL on port 5432 (internal)
- **Backend API**: Strapi on port 1337 (internal/external)

## Docker Compose Best Practices

### Environment Variables
```yaml
environment:
  NODE_ENV: production
  DATABASE_HOST: database  # Service name as hostname
  DATABASE_PORT: 5432
  STRAPI_TELEMETRY_DISABLED: true
  HOST: 0.0.0.0
```

### Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:1337/api/get-tips"]
  interval: 30s
  timeout: 10s
  retries: 5
  start_period: 60s
```

### Service Dependencies
```yaml
depends_on:
  database:
    condition: service_healthy
  backend:
    condition: service_healthy
```

## Dockerfile Optimization

### Frontend Dockerfile
```dockerfile
FROM node:22.14.0-alpine AS builder

# Install system dependencies
RUN apk add --no-cache python3 make g++ git curl

# Set working directory
WORKDIR /app

# Configure npm registry
RUN npm config set registry https://registry.npmmirror.com/

# Install pnpm
RUN npm install -g pnpm
RUN pnpm config set registry https://registry.npmmirror.com/

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build application
RUN pnpm run build

# Production stage
FROM node:22.14.0-alpine AS production

WORKDIR /app

# Copy built application
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules

# Expose port
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
  CMD curl -f http://localhost:4000 || exit 1

# Start application
CMD ["pnpm", "run", "start"]
```

### Backend Dockerfile
```dockerfile
FROM node:22.14.0-alpine AS builder

# Install system dependencies
RUN apk add --no-cache python3 make g++ git curl

WORKDIR /app

# Configure npm registry
RUN npm config set registry https://registry.npmmirror.com/

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Production stage
FROM node:22.14.0-alpine AS production

# Install curl for health checks
RUN apk add --no-cache curl

WORKDIR /app

# Copy dependencies
COPY --from=builder /app/node_modules ./node_modules

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p public/uploads

# Build Strapi
RUN npm run build

# Expose port
EXPOSE 1337

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
  CMD curl -f http://localhost:1337/api/get-tips || exit 1

# Start application
CMD ["npm", "start"]
```

## Volume Management

### Data Persistence
```yaml
volumes:
  postgres_data:
    driver: local
  backend_uploads:
    driver: local
  backend_data:
    driver: local
```

### Volume Mounting
```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
  - backend_uploads:/app/public/uploads
  - backend_data:/app/.tmp
```

## Environment Configuration

### Production Environment
```bash
# Production environment variables
NODE_ENV=production
STRAPI_TELEMETRY_DISABLED=true
HOST=0.0.0.0

# Database configuration
DATABASE_CLIENT=postgres
DATABASE_HOST=database
DATABASE_PORT=5432
DATABASE_NAME=fortune_telling
DATABASE_USERNAME=strapi
DATABASE_PASSWORD=strong_password_here
DATABASE_SSL=false

# JWT configuration
JWT_SECRET=your-secure-jwt-secret-256-bits
ADMIN_JWT_SECRET=your-secure-admin-jwt-secret-256-bits
API_TOKEN_SALT=your-secure-api-token-salt-256-bits
TRANSFER_TOKEN_SALT=your-secure-transfer-token-salt-256-bits
APP_KEYS=key1,key2,key3,key4

# AI API configuration
OPENAI_API_KEY=sk-your-deepseek-api-key
OPENAI_BASE_URL=https://api.deepseek.com/v1

# Service ports
BACKEND_PORT=1337
```

### Development Environment
```bash
# Development overrides
NODE_ENV=development
DATABASE_CLIENT=sqlite
DATABASE_FILENAME=.tmp/data.db

# Development API keys (non-production)
OPENAI_API_KEY=sk-development-key
```

## Security Configuration

### PostgreSQL Security
```yaml
postgres:
  environment:
    POSTGRES_DB: ${DATABASE_NAME}
    POSTGRES_USER: ${DATABASE_USERNAME}
    POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
    POSTGRES_INITDB_ARGS: "--auth-host=md5"
  volumes:
    - postgres_data:/var/lib/postgresql/data
  restart: unless-stopped
```

### Network Security
```yaml
networks:
  default:
    driver: bridge
  internal:
    driver: bridge
    internal: true
```

### Container Security
```dockerfile
# Run as non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

USER nextjs
```

## Resource Management

### Memory Limits
```yaml
deploy:
  resources:
    limits:
      memory: 512M
    reservations:
      memory: 256M
```

### CPU Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
```

## Logging Configuration

### Centralized Logging
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Log Rotation
```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
        compress: "true"
```

## Monitoring & Health Checks

### Application Health
```javascript
// Health check endpoint
app.get('/health', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    ai: await checkAI(),
    timestamp: new Date().toISOString()
  };
  
  res.json({ status: 'healthy', checks });
});
```

### Database Health
```javascript
const checkDatabase = async () => {
  try {
    await strapi.db.connection.raw('SELECT 1');
    return { status: 'healthy' };
  } catch (error) {
    return { status: 'unhealthy', error: error.message };
  }
};
```

## Backup & Recovery

### Database Backup
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="fortune_telling_backup_$DATE.sql"

docker exec fortune-telling-db pg_dump \
  -U strapi \
  -d fortune_telling \
  > backups/$BACKUP_NAME

# Compress backup
gzip backups/$BACKUP_NAME
```

### Volume Backup
```bash
# Backup volumes
docker run --rm \
  -v fortune-telling_postgres_data:/data \
  -v $(pwd)/backups:/backups \
  alpine \
  tar czf /backups/postgres_data_backup.tar.gz /data
```

## Deployment Strategies

### Blue-Green Deployment
```yaml
version: '3.8'
services:
  frontend-blue:
    # Blue environment
  frontend-green:
    # Green environment
  
  nginx:
    # Load balancer
```

### Rolling Updates
```bash
# Update strategy
docker-compose pull
docker-compose up -d --no-deps --scale frontend=2 frontend
docker-compose up -d --no-deps --scale frontend=1 frontend
```

## Performance Optimization

### Image Optimization
```dockerfile
# Multi-stage build
FROM node:22.14.0-alpine AS deps
# Install dependencies

FROM node:22.14.0-alpine AS builder
# Build application

FROM node:22.14.0-alpine AS runner
# Runtime environment
```

### Caching Strategy
```dockerfile
# Layer caching
COPY package*.json ./
RUN npm ci --only=production

# Source code (changes frequently)
COPY . .
```

## Production Deployment

### CI/CD Pipeline
```yaml
# GitHub Actions example
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        run: |
          docker-compose -f docker-compose.prod.yml pull
          docker-compose -f docker-compose.prod.yml up -d
```

### SSL Configuration
```yaml
# Traefik or nginx proxy
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.fortune-telling.rule=Host(`ft.fangyuanxiaozhan.com`)"
  - "traefik.http.routers.fortune-telling.tls=true"
  - "traefik.http.routers.fortune-telling.tls.certresolver=letsencrypt"
```

## Troubleshooting

### Common Issues
1. **Port Conflicts**: Check if ports 4000/1337 are available
2. **Database Connection**: Verify database health and credentials
3. **API Keys**: Ensure OpenAI API key is valid
4. **Memory Issues**: Monitor container memory usage

### Debug Commands
```bash
# Check container logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database

# Container shell access
docker-compose exec backend sh
docker-compose exec frontend sh

# Database access
docker-compose exec database psql -U strapi -d fortune_telling
```

### Performance Monitoring
```bash
# Monitor resource usage
docker stats

# Check container health
docker-compose ps
```

## Maintenance Tasks

### Regular Updates
```bash
# Update containers
docker-compose pull
docker-compose up -d

# Clean up unused images
docker system prune -a
```

### Database Maintenance
```bash
# Vacuum database
docker-compose exec database psql -U strapi -d fortune_telling -c "VACUUM ANALYZE;"

# Check database size
docker-compose exec database psql -U strapi -d fortune_telling -c "SELECT pg_size_pretty(pg_database_size('fortune_telling'));"
``` 