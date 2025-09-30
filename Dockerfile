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

# Set default environment variables (can be overridden at runtime)
ENV PORT=9000
ENV DB_URI=${DB_URI}
ENV DB_USERNAME=${DB_USERNAME}
ENV DB_PASSWORD=${DB_PASSWORD}

# Switch to non-root user
USER nodejs

# Expose the correct port (app listens on 9000, not 4000)
EXPOSE 9000

# Run Apollo server
CMD ["node", "index.js"]
