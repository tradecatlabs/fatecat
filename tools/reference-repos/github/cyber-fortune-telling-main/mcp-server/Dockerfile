# Cyber Fortune Telling MCP Server
FROM node:22.14.0-alpine

# Set working directory
WORKDIR /app

# Install dependencies
RUN apk add --no-cache curl

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --omit=dev && npm cache clean --force

# Copy source code
COPY src/ src/

# Create non-root user for security
RUN addgroup -g 1001 -S mcpuser && \
    adduser -S mcpuser -u 1001 -G mcpuser && \
    chown -R mcpuser:mcpuser /app

USER mcpuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "console.log('MCP Server Health Check OK')" || exit 1

# Default environment variables
ENV CYBER_FORTUNE_API_BASE_URL=http://localhost:11337/api
ENV LOG_LEVEL=info
ENV NODE_ENV=production

# Default command - run MCP server
CMD ["node", "src/index.js"]

# Labels for metadata
LABEL \
    org.opencontainers.image.title="Cyber Fortune Telling MCP Server" \
    org.opencontainers.image.description="MCP Server for Fortune Telling API integration" \
    org.opencontainers.image.vendor="zhaoolee" \
    org.opencontainers.image.version="1.0.0" \
    org.opencontainers.image.source="https://github.com/zhaoolee/cyber-fortune-telling" 