# DAS Serverless Functions

Serverless Functions offer an innovative approach to cloud computing, enabling developers to execute code without worrying about managing underlying infrastructure. This architecture allows for the granular execution of code snippets, scaling efficiently according to demand.

## Pre-Commit Setup

To ensure code quality before pushing changes, it's recommended to set up pre-commit hooks that run automated tests locally. Run this command once:

```bash
pre-commit install
```

## OpenFaaS: Simplified Serverless Functions Management

[OpenFaaS](https://www.openfaas.com/) (Open Functions as a Service) is an open-source platform designed to simplify the deployment and management of serverless functions. It supports flexible deployments in both cloud and local environments, providing a robust framework for developing and running functions at scale.

## Running an OpenFaaS Function Locally

### Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Architecture Overview

![Architecture](./docs/images/local-architecture.jpg)

The local architecture includes the following components:

- **Redis & MongoDB**: Databases used by the application.
- **Metta Parser**: A temporary container to load initial data into Redis and MongoDB.
- **OpenFaaS**: Primary container running OpenFaaS and the `faas-cli`.
- **Function Container**: Internal container responsible for processing function requests.
- **das-query-engine**: Operates on the same Docker network as the `openfaas` container.
- **Port 8080**: Exposed for host machine access.

### Step-by-Step Guide

1. **Clone the Project**

   Begin by cloning the repository:

   ```bash
   git clone <REPOSITORY_URL>
   cd <PROJECT_NAME>
   ```

2. **Create an Environment File**

   Copy the example `.env` file and modify it with your environment-specific configurations:

   ```bash
   cp .env.example .env
   ```

3. **Start the Environment**

   Use the following command to start the necessary services:

   ```bash
   make serve
   ```

   This command initializes containers for Redis, MongoDB, and the temporary `das-metta-parser` container to load initial data. Afterward, the `openfaas` container will start, which includes the `faas-cli`.

4. **Execute the Function**

   After the environment is set up, you can execute the OpenFaaS function through two methods:

   **Option 1: Using the OpenFaaS Desktop Client**

   Launch the desktop client with:

   ```bash
   make start-faas-client
   ```

   In the client interface:
   - Ensure the URL is set to `http://localhost:8080`.
   - Enter the function name.
   - Input the request body (JSON format).
   - Send the request and review the response.

   **Option 2: Using Curl**

   You can also trigger the function using `curl`. Since the function processes binary data, ensure the request uses the correct headers and data format:

   ```bash
   curl -X POST \
     -H "Content-Type: application/octet-stream" \
     --data-binary "@/tmp/data.pkl" \
     http://localhost:8080
   ```

   Replace `/tmp/data.pkl` with the actual path to your serialized (pickle format) data.

5. **Stop the Environment**

   To shut down and clean up your environment, run:

   ```bash
   make stop
   ```

### Using `hyperon-das` and `hyperon-das-atomdb` Locally

This feature allows developers to integrate the AtomDB and Query Engine packages locally without needing to publish them on PyPI, facilitating faster testing during development.

1. Open the `.env` file.
2. Add the following environment variables, updating the paths as necessary:

   ```dotenv
   ATOMDB_PACKAGE_PATH=/home/user/Documents/das-atom-db/hyperon_das_atomdb
   QUERY_ENGINE_PACKAGE_PATH=/home/user/Documents/das-query-engine/hyperon_das
   ```

   Ensure these paths point directly to the `hyperon_das_atomdb` and `hyperon_das` modules within your project directory. For example:

   ```
   /das-atom-db/
   ├── hyperon_das_atomdb/
   │   └── ...
   │
   /das-query-engine/
   ├── hyperon_das/
   │   └── ...
   ```

   This ensures that the environment variables point directly to the modules within your project structure.

3. If you'd prefer to use the latest versions from PyPI, leave these variables empty:

   ```dotenv
   ATOMDB_PACKAGE_PATH=
   QUERY_ENGINE_PACKAGE_PATH=
   ```

## Makefile Commands

The `Makefile` includes several commands to streamline development and testing processes. Here’s a summary of the key commands:

### Formatting and Linting

- `make isort`: Sorts imports in the codebase.
- `make black`: Formats code using [Black](https://black.readthedocs.io/en/stable/).
- `make flake8`: Lints the code with [Flake8](https://flake8.pycqa.org/en/latest/).
- `make lint`: Runs `isort`, `black`, and `flake8` in sequence.

### Testing

- `make unit-tests`: Runs the unit tests.
- `make unit-tests-coverage`: Runs unit tests with code coverage reporting.
- `make integration-tests`: Builds the project and runs the integration tests.

### Building and Running

- `make build`: Rebuilds Docker containers without cache.
- `make serve`: Starts services via Docker Compose, recreating containers as needed.
- `make stop`: Stops and removes the Docker containers.

### Other Commands

- `make pre-commit`: Runs linters and tests (unit + integration) before commit.
- `make start-faas-client`: Launches the OpenFaaS desktop client.

To execute any of these commands, simply run:

```bash
make <command>
```

Replace `<command>` with the desired task (e.g., `serve`, `lint`).
