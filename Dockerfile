\
        # Dockerfile for Render (Linux)
        FROM python:3.11-slim

        # Install system deps
        RUN apt-get update && apt-get install -y --no-install-recommends \
            build-essential curl git ca-certificates libssl-dev pkg-config && rm -rf /var/lib/apt/lists/*

        # Install Rust (for spec-kit-mcp)
        RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        ENV PATH="/root/.cargo/bin:${PATH}"

        # Install spec-kit-mcp via cargo
        RUN cargo install spec-kit-mcp

        WORKDIR /app

        COPY requirements.txt ./
        RUN pip install --no-cache-dir -r requirements.txt

        # Copy app
        COPY . /app

        EXPOSE 3000

        CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
