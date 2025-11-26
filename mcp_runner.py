\
        import subprocess
        import asyncio
        from mcp.client import Client
        from mcp.transport.stdio import StdioTransport
        import tempfile
        import json
        import os
        import time


        async def _call_tool_via_mcp(tool: str, params: dict):
            # Start spec-kit-mcp (assumes it's in PATH)
            proc = subprocess.Popen(["spec-kit-mcp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Give server a moment to initialize
            time.sleep(2)

            transport = StdioTransport(proc.stdin, proc.stdout)
            client = Client("speckit-wrapper", "1.0")
            await client.connect(transport)

            # Call tool
            response = await client.call_tool(tool, params or {})

            # Clean up
            try:
                proc.kill()
            except Exception:
                pass

            return response


        async def run_speckit_tool(tool: str, prompt: str = None):
            params = {"prompt": prompt} if prompt else {}
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(_call_tool_via_mcp(tool, params))

            # Normalize response to dict with json, markdown, files
            out = {}
            if isinstance(response, dict):
                out.update(response)
            else:
                out["raw"] = str(response)
            return out
