# ---- Base Python image ----
FROM python:3.9-slim

WORKDIR /app

# ---- Install system deps (Node + npm) ----
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# ---- Copy dependency files first (better caching) ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY package*.json ./
RUN npm install

# ---- Copy the rest of the project ----
COPY . .

# ---- Build TypeScript ----
RUN npm run build

# ---- Run Flask ----
CMD ["flask", "run", "--host=0.0.0.0", "--port=80", "--debug", "--reload"]