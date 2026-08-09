🎬 Indian Film Industry Analytics Pipeline
A Python + PostgreSQL analytics pipeline that loads Indian movie data, computes profitability/ROI metrics, runs SQLAlchemy-based analysis, and generates a Matplotlib dashboard (All-India vs Telugu comparisons).

What it does:
Step 1 — Load & Clean (load_data.py)
	•	Loads data/Movie_Data.csv
	•	Renames columns into a consistent schema
	•	Converts numeric fields (coerce errors to null)
	•	Drops rows missing budget or revenue
	•	Computes:
	•	profit = revenue - budget
	•	roi = ((revenue - budget) / budget) * 100
	•	profitable = profit > 0
	•	Pushes the cleaned dataset into PostgreSQL table: movies

Step 2 — Analysis (analyse.py)
Runs database-backed analysis via SQLAlchemy ORM:
	•	Genre performance (count, avg ROI, avg revenue, avg IMDb)
	•	Hit rate by genre (% profitable)
	•	Top 10 movies by profit
	•	Biggest losses (top 10 unprofitable)

Outputs are printed as formatted tables in the console.

Step 3 — Dashboard (visualise.py)
Builds a 6-panel dashboard comparing:
	•	Top 10 grossing (All India)
	•	Top 10 grossing (Telugu subset)
	•	Avg revenue by genre (All India)
	•	Avg revenue by genre (Telugu)
	•	Hit rate by genre (All India)
	•	Hit rate by genre (Telugu)

Saves image to:
	•	outputs/dashboard.png

🧰 Tech Stack
	•	Python
	•	Pandas
	•	PostgreSQL
	•	SQLAlchemy
	•	psycopg2
	•	Matplotlib

📁 Project Structure
indian_film_pipeline/
├── main.py
├── load_data.py
├── analyse.py
├── visualise.py
├── mcp_server.py
├── config.py
├── .env.example
├── requirements.txt
├── data/
│   └── Movie_Data.csv
└── outputs/
    └── dashboard.png

🔌 MCP Layer
mcp_server.py exposes the analysis layer as read-only tools over FastMCP
(stdio transport), so an MCP client -- Claude Desktop, Claude Code, etc. --
can query the pipeline directly instead of running main.py and reading
console output.

Tools exposed:
	•	get_genre_performance
	•	get_hit_rate_by_genre
	•	get_top_movies_by_profit(limit)
	•	get_biggest_losses(limit)
	•	generate_dashboard -- regenerates outputs/dashboard.png, returns its path

The ETL step (load_data.py) is deliberately NOT exposed as a tool. An MCP
client can query the movies table but can never reload or overwrite it --
run `python main.py` or `python load_data.py` yourself when you want to
refresh the data.

Setup:
	1.	./setup.sh -- creates .venv, installs requirements, scaffolds .env
	2.	Edit .env with your Postgres credentials
	3.	source .venv/bin/activate && python main.py -- loads data, run once
	4.	Connect an MCP client (see below)

Connecting a client:

Claude Code -- a project-scoped .mcp.json is already in this folder. Open
Claude Code from inside indian_film_pipeline/ and it will pick the server
up automatically (you'll be prompted to approve it on first use).

Claude Desktop -- edit
~/Library/Application Support/Claude/claude_desktop_config.json
and add this under "mcpServers" (create the file/key if it doesn't exist),
then fully quit and reopen Claude Desktop:

    "indian-film-pipeline": {
      "command": "/Users/bharghavkarnati6/Library/CloudStorage/OneDrive-UniversityofNewBrunswick/indian_film_pipeline/.venv/bin/python3",
      "args": [
        "/Users/bharghavkarnati6/Library/CloudStorage/OneDrive-UniversityofNewBrunswick/indian_film_pipeline/mcp_server.py"
      ]
    }

Sanity-check the server on its own before connecting a client:
    source .venv/bin/activate && python mcp_server.py
(it will sit there waiting for stdio input -- Ctrl+C to exit. That's
expected; it only speaks JSON-RPC, not a REPL.)


