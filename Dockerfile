# Use a lightweight Python base image
FROM python:3.13-slim AS base

# Install uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy only the files needed for installing dependencies to maximize cache hits
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures the lockfile is used without modification
# --no-install-project skips installing the project itself (source code) for better caching
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application code
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev

# Ensure the virtual environment is used
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# --- Stage for Agent ---
FROM base AS agent
# The user wants 8080:8000 mapping, so the container listens on 8000
EXPOSE 8000
CMD ["uv", "run", "adk", "web", "agents", "--host", "0.0.0.0"]

# --- Stage for API ---
FROM base AS api
EXPOSE 8000
# The user wants 8000:8000 mapping, so the container listens on 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
