#!/bin/bash
# One-time setup: venv + dependencies + .env scaffold.
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example -- fill in your Postgres credentials before running the ETL."
fi

echo "Setup complete."
echo "Next steps:"
echo "  1. Edit .env with your Postgres credentials"
echo "  2. source .venv/bin/activate && python main.py   # loads data, one time"
echo "  3. Connect mcp_server.py to your MCP client (see README.md)"
