# Travel Destinations — Docker Containerization

## 1. Project Overview

Travel Destinations is an existing web application built with:

- **Backend:** Python / Flask
- **Frontend:** TypeScript, HTML and CSS
- **Database:** MariaDB (MySQL-compatible)

The goal was to containerize the existing application using Docker and Docker Compose, making it portable and easier to deploy on different computers.
I have redone the already existing project i've had from before to be more in line with assignement, hence a new branch.

## 2. Dockerfile — Multi-Stage Build

The Dockerfile uses **two stages** to separate the frontend build process from the application runtime.

### Stage 1 — Frontend Builder (Node.js)

- Uses a lightweight Node.js image.
- Installs dependencies with `npm ci` for reproducible builds.
- Compiles TypeScript into JavaScript using `tsc`.
- Docker layer caching avoids reinstalling dependencies when only source code changes.

### Stage 2 — Flask Runtime (Python)

- Uses a lightweight Python image.
- Installs Flask and the required Python packages.
- Copies only the compiled frontend files from Stage 1, leaving Node.js, npm and build dependencies out of the final image.
- Runs Flask as a **non-root user (`appuser`)** for improved security.
- Exposes port 8000 for the web application.

**Why multi-stage?** It separates build tools from runtime dependencies, reducing the final image size and unnecessary components.

## 3. Docker Compose

`docker-compose.yml` defines three services:

| Service | Purpose |
|---|---|
| `web` | Flask application, accessible on port 8000 |
| `mariadb` | Database, accessible internally |
| `phpmyadmin` | Database administration, accessible on port 8080 |

Docker Compose manages the services together using one YAML configuration file.

### Named Network

`travel_destinations_network` connects the containers. Flask accesses MariaDB using the service hostname `mariadb`, without exposing the database port to the host.

### Named Volume

`travel_destinations_data` stores MariaDB data outside the container, so database records survive container recreation.

### Environment Variables

Database credentials are supplied using a local `.env` file rather than hardcoded in the Python source or Dockerfile. The `.env` file is excluded from Git - the only thing it contains is DB_PASSWORD.

## 4. Running the Project

Requirements: **Git and Docker Desktop**.

1. Clone the repo from docker-containerization branch and set the current directory to travel_destinations

```bash
git clone -b docker-containerization https://github.com/pinzdesign/travel_destinations.git
cd travel_destinations
```

2. IMPORTANT: Create a `.env` file containing:

```dotenv
DB_PASSWORD=some_password
```

Build and start the containers:

```bash
docker compose up --build
```
That's basically it, no need to install anything separately

Access the application:

- Website: http://localhost:8000
- phpMyAdmin: http://localhost:8080

Stop the containers, when needed:

```bash
docker compose down
```

The named database volume is preserved when stopping the application.

**Database setup:** Import the provided SQL database file.

## 5. Testing and Results

- Docker image built successfully using two stages.
- Verified the container runs as `appuser`, not root. (The old "main" version runs as root)
- Flask, MariaDB and phpMyAdmin started using Docker Compose.
- Confirmed the named network and database volume were created.
- Easily deployed the application on my second computer.
- Imported the database and verified that records appear on the website.

## 6. Conclusion

Docker makes the application portable and reproducible without requiring Python, Node.js or MariaDB to be installed individually on the host.
