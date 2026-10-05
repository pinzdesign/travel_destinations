# ============================================================
# Stage 1: Build the TypeScript frontend
# ============================================================
FROM node:22-alpine AS frontend-builder

WORKDIR /build

# Copy dependency files first to take advantage of Docker caching
COPY package.json package-lock.json ./

# Install exact dependencies from package-lock.json
RUN npm ci

# Copy TypeScript configuration and source files
COPY tsconfig.json ./
COPY frontend/ ./frontend/

# Compile TypeScript: frontend/ -> static/
RUN npm run build

# ============================================================
# Stage 2: Python runtime
# ============================================================
FROM python:3.9-slim AS runtime

WORKDIR /app

# Copy Python dependency file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY app.py x.py ./
COPY templates/ ./templates/

# Copy the compiled TypeScript output from the builder stage
COPY --from=frontend-builder /build/static ./static

# Create a non-root user and give it ownership of the application
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Run the application as the non-root user
USER appuser

EXPOSE 8000

# Start the Flask application
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8000"]