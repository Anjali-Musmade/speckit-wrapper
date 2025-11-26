import subprocess
import asyncio
import time

from mcp.client.stdio import StdioClient


async def run_speckit_tool(tool: str, prompt: str = None):
    """
    Launch spec-kit-mcp, connect using the modern MCP StdioClient,
    execute the tool, return results.
    """

    # Start MCP server
    proc = subprocess.Popen(
        ["spec-kit-mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Small delay to ensure server initializes
    time.sleep(2)

    # Connect via STDIO
    client = StdioClient(
        proc.stdin,
        proc.stdout,
        name="speckit-wrapper",
        version="1.0"
    )
    await client.start()

    # Prepare params
    params = {"prompt": prompt} if prompt else {}

    # Call tool
    result = await client.call_tool(tool, params)

    # Cleanup
    try:
        proc.kill()
    except:
        pass

    return result
