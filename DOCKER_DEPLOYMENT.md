# Docker Deployment Guide for Resume Tailor

This guide explains how to deploy the Resume Tailor application using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your system
- OpenAI API key

## Deployment Steps

### 1. Configure Environment Variables

Make sure your `.env` file is properly configured with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
```

### 2. Build and Start the Docker Container

From the project root directory, run:

```bash
docker-compose up -d --build
```

This command will:
- Build the Docker image for the application
- Start the container in detached mode (-d)
- Map port 5000 on your host to port 5000 in the container

### 3. Verify the Application is Running

Open your web browser and navigate to:

```
http://localhost:5000
```

You should see the Resume Tailor application running.

### 4. View Logs

To view the application logs:

```bash
docker-compose logs -f
```

Press `Ctrl+C` to exit the log view.

### 5. Stop the Application

To stop the application:

```bash
docker-compose down
```

## Troubleshooting

### API Key Issues

If you encounter issues with the OpenAI API key:

1. Make sure your `.env` file contains the correct API key
2. Restart the container after updating the `.env` file:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### Port Conflicts

If port 5000 is already in use on your system:

1. Edit the `docker-compose.yml` file and change the port mapping:
   ```yaml
   ports:
     - "8080:5000"  # Change 5000 to another port like 8080
   ```
2. Restart the container:
   ```bash
   docker-compose down
   docker-compose up -d
   ```
3. Access the application at `http://localhost:8080`

## Production Deployment Considerations

For production deployment, consider:

1. Using a reverse proxy like Nginx for SSL termination
2. Setting up proper monitoring and logging
3. Implementing a more robust database solution if needed
4. Using Docker Swarm or Kubernetes for container orchestration
