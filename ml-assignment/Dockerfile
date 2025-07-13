# Multi-stage Dockerfile for ML Feature Engineering API
# Stage 1: Build documentation server
FROM node:18-alpine AS docs-builder

# Set working directory for docs
WORKDIR /app/docs

# Copy package files
COPY docs/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy docs source code
COPY docs/ ./

# Stage 2: Main application with Python and Node.js
FROM node:18-alpine AS final

# Install Python and pip
RUN apk add --no-cache python3 py3-pip python3-dev build-base

# Set working directory
WORKDIR /app

# Copy Python requirements
COPY requirements.txt .

# Create virtual environment and install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application files
COPY main.py .
COPY data_analysis.py .
COPY test_api.py .

# Copy documentation server from builder stage
COPY --from=docs-builder /app/docs ./docs

# Create directory for data files
RUN mkdir -p ml-assignment
COPY ml-assignment/ ./ml-assignment/

# Copy other project files
COPY *.csv ./
COPY *.md ./
COPY *.sh ./
COPY *.bat ./

# Expose ports
EXPOSE 8002 5002

# Create startup script
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'export PATH="/opt/venv/bin:$PATH"' >> /app/start.sh && \
    echo 'cd /app/docs && npm start &' >> /app/start.sh && \
    echo 'cd /app && python main.py &' >> /app/start.sh && \
    echo 'wait' >> /app/start.sh && \
    chmod +x /app/start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8002/health || exit 1

# Run the application
CMD ["/app/start.sh"] 