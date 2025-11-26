import subprocess
import asyncio
import time
from mcp import MCP

async def run_speckit_tool(tool: str, prompt: str = None):
    """
    Starts spec-kit-mcp using a subprocess, connects as an MCP client,
    calls the requested tool, and returns the JSON result.
    """

    # Start the MCP server
    proc = subprocess.Popen(
        ["spec-kit-mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for server to start
    time.sleep(2)

    # Connect to MCP server
    mcp = MCP()
    await mcp.start(stdio=(proc.stdin, proc.stdout))

    # Run tool
    params = {"prompt": prompt} if prompt else {}
    result = await mcp.call_tool(tool, params)

    # Shutdown
    try:
        proc.kill()
    except:
        pass

    return result
