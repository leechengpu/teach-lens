#!/usr/bin/env bash
set -e

if [ ! -d ".venv" ]; then
  echo "Creating Python venv..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

mkdir -p data data/audio

if [ ! -f "data/teachlens.db" ]; then
  echo "Initializing SQLite DB..."
  sqlite3 data/teachlens.db < schemas/create_tables.sql
  if [ -f "tests/demo_data.sql" ]; then
    sqlite3 data/teachlens.db < tests/demo_data.sql
  fi
fi

echo ""
echo "Setup complete. Run:"
echo "  source .venv/bin/activate"
echo "  streamlit run app.py"
