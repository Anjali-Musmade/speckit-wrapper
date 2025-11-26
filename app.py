        from fastapi import FastAPI
        from pydantic import BaseModel
        from mcp_runner import run_speckit_tool
        from git_commit import auto_commit
        from typing import Optional

        app = FastAPI()

        class SpeckitRequest(BaseModel):
            tool: str
            prompt: Optional[str] = None
            repo_url: Optional[str] = None
            repo_branch: Optional[str] = "main"
            repo_path: Optional[str] = None
            auto_commit: bool = False

        @app.post("/run")
        async def run_tool(req: SpeckitRequest):
            # Run MCP tool
            result = await run_speckit_tool(req.tool, req.prompt)

            # If results include files and user asked for commit
            if req.auto_commit and req.repo_url and req.repo_path:
                commit_res = auto_commit(req.repo_url, req.repo_branch, req.repo_path, result.get("files", []))
            else:
                commit_res = None

            return {
                "status": "success",
                "tool": req.tool,
                "prompt": req.prompt,
                "result": result,
                "commit": commit_res,
            }
