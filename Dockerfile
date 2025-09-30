# Use Node.js Alpine image for smaller size and better security
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy package files first for better caching
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --omit=dev --legacy-peer-deps && npm cache clean --force

# Copy application code
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

# Expose the correct port (app listens on 9000, not 4000)
EXPOSE 9000

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:9000/.well-known/apollo/server-health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) })"

# Run Apollo server
CMD ["node", "index.js"]
