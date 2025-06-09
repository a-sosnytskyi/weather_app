# Weather Application Deployment Guide

## Prerequisites

For convenience, it's recommended to install `make` utility on your system.

## Deployment Steps

### Option 1: Using Make (Recommended)

```bash
# 1. Create Docker network
make docker-create-network

# 2. Build application containers
make app-build

# 3. Start application (foreground)
make app-up

# OR start in background (detached mode)
make app-up-d
```

### Option 2: Manual Docker Commands

```bash
# 1. Create Docker network
docker network create weather_app_network

# 2. Build application containers
docker compose build

# 3. Start application
docker compose up --remove-orphans

# OR start in background
docker compose up -d --remove-orphans
```

## Available Make Commands

- `make docker-create-network` - Create Docker network for the application
- `make app-build` - Build all application containers
- `make app-up` - Start application in foreground mode
- `make app-up-d` - Start application in detached (background) mode
- `make app-stop` - Stop the application containers

## Notes

- The application requires a dedicated Docker network (`weather_app_network`)
- Use `--remove-orphans` flag to clean up any unused containers
- For development, use `make app-up` to see logs in real-time
- For production-like deployment, use `make app-up-d` to run in background