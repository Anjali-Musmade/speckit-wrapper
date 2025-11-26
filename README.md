\
        # speckit-wrapper

        This project implements a simple REST wrapper around the Speckit MCP server, enabling you to call Speckit tools via HTTP.

        ## Local testing

        1. Install Python 3.11 and Rust (cargo).
        2. Build the spec-kit-mcp binary with `cargo install spec-kit-mcp` (or let the Dockerfile install it).
        3. Create a virtualenv and install python deps:

        ```bash
        python -m venv .venv
        source .venv/bin/activate
        python -m pip install -r requirements.txt
        ```

        4. Run locally:

        ```bash
        uvicorn app:app --reload --host 0.0.0.0 --port 3000
        ```

        5. Test with curl:

        ```bash
        curl -X POST http://localhost:3000/run -H "Content-Type: application/json" -d '{"tool":"specify","prompt":"Generate a test spec"}'
        ```

        ## Deploy to Render

        1. Push repository to GitHub.
        2. Create a new Web Service on Render, connect the repo, choose Docker, Free plan.
        3. Deploy — Render will build the Dockerfile and run the app.

        ## Use from Azure DevOps

        Call the endpoint with `curl` as shown in `azure-pipeline.yml` snippet.
