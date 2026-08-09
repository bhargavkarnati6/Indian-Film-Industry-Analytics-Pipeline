"""
FastMCP server exposing the Indian Film Industry Analytics Pipeline as
read-only tools an MCP client (Claude Desktop, Claude Code, etc.) can call.

Deliberately does NOT expose the ETL step (load_data.py) -- this server can
query the `movies` table but never reload or overwrite it. Run the ETL
manually via `python main.py` or `python load_data.py` when you want to
refresh the data.

Run:
    python mcp_server.py

Then point your MCP client at this file (stdio transport).
"""
import contextlib
import io

from fastmcp import FastMCP

from analyse import (
    genre_performance,
    hit_rate_by_genre,
    top_10_by_profit,
    biggest_losses,
)
from visualise import get_data, build_dashboard

mcp = FastMCP("Indian Film Industry Analytics")


def _quiet(fn, *args, **kwargs):
    """Run a pipeline function with stdout captured.

    The analysis functions print formatted tables for CLI use. Under stdio
    transport, MCP's JSON-RPC messages travel over stdout too -- any stray
    print() would corrupt the protocol stream. This swallows those prints
    so only the tool's JSON return value goes out.
    """
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = fn(*args, **kwargs)
    return result


@mcp.tool
def get_genre_performance() -> list[dict]:
    """Movie count, avg ROI, avg revenue, and avg IMDb rating per genre,
    ordered by average ROI descending."""
    df = _quiet(genre_performance)
    return df.to_dict(orient="records")


@mcp.tool
def get_hit_rate_by_genre() -> list[dict]:
    """Percentage of profitable movies per genre, ordered by hit rate
    descending."""
    df = _quiet(hit_rate_by_genre)
    return df.to_dict(orient="records")


@mcp.tool
def get_top_movies_by_profit(limit: int = 10) -> list[dict]:
    """The most profitable movies in the dataset, ranked by absolute profit
    (revenue - budget)."""
    df = _quiet(top_10_by_profit, limit=limit)
    return df.to_dict(orient="records")


@mcp.tool
def get_biggest_losses(limit: int = 10) -> list[dict]:
    """The least profitable (or most unprofitable) movies in the dataset,
    ranked by loss size."""
    df = _quiet(biggest_losses, limit=limit)
    return df.to_dict(orient="records")


@mcp.tool
def generate_dashboard() -> str:
    """Regenerate the 6-panel Matplotlib dashboard (All-India vs Telugu
    comparisons) from the current database contents and save it to
    outputs/dashboard.png. Returns the path to the saved image."""
    all_movies, telugu = _quiet(get_data)
    _quiet(build_dashboard, all_movies, telugu)
    return "outputs/dashboard.png"


if __name__ == "__main__":
    mcp.run()
