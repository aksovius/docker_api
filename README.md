# Docker API Server

This is a Python API server that uses FastAPI and Strawberry to provide Docker container controlling and monitoring endpoints. It uses the Docker SDK to interact with the Docker API and provides additional endpoints for NVIDIA monitoring.

## Features

- List, start, stop, and remove Docker containers
- Get container logs and stats
- List and monitor NVIDIA GPUs

## Technologies

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [Strawberry](https://strawberry.rocks/): A GraphQL library for Python that is based on dataclasses and provides a code-first approach to schema definition.
- [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/): A Python library for the Docker Engine API.
- [NVIDIA System Management Interface (nvidia-smi)](https://developer.nvidia.com/nvidia-system-management-interface): A tool used for monitoring NVIDIA GPUs.

## Usage

1. Clone this repository.
2. Install the required packages with `pip install -r requirements.txt`.
3. Start the server with `python app.py`.

### Endpoints

- `/containers`: List all running containers
- `/containers/{id}`: Get details for a specific container
- `/containers/{id}/logs`: Get logs for a specific container
- `/containers/{id}/stats`: Get stats for a specific container
- `/containers/{id}/start`: Start a specific container
- `/containers/{id}/stop`: Stop a specific container
- `/containers/{id}/remove`: Remove a specific container
- `/gpus`: List all NVIDIA GPUs
- `/gpus/{id}/stats`: Get stats for a specific NVIDIA GPU

## License

This project is licensed under the MIT License - see the LICENSE file for details.
