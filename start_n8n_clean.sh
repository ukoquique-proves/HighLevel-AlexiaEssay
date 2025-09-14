#!/bin/bash
# start_n8n_clean.sh - Robust n8n startup script v2
# Usage: bash start_n8n_clean.sh

PORT=5678
N8N_DATA_DIR="$(pwd)/n8n-data"
LOG_FILE="$(pwd)/n8n.log"

echo "[INFO] --- n8n Startup Script --- "

# 1. Check for n8n in PATH
if ! command -v n8n &> /dev/null; then
  echo "[ERROR] n8n is not installed or not in your PATH. Please install n8n first."
  exit 1
fi
echo "[OK] n8n command found."

# 2. Kill any process using the n8n port
# The '|| true' prevents the script from exiting if no process is found
PID=$(lsof -ti tcp:$PORT || true)
if [ ! -z "$PID" ]; then
  echo "[INFO] Killing process using port $PORT (PID: $PID)"
  kill -9 $PID
  sleep 1 # Give the port a moment to be released
else
  echo "[INFO] Port $PORT is free. No process to kill."
fi

# 3. Create data directory if it doesn't exist
if [ ! -d "$N8N_DATA_DIR" ]; then
  echo "[INFO] Creating n8n data directory at $N8N_DATA_DIR"
  mkdir -p "$N8N_DATA_DIR"
fi

# 4. Start n8n in background with custom data dir and log output
export N8N_USER_FOLDER="$N8N_DATA_DIR"
echo "[INFO] Starting n8n on port $PORT..."

# Clear previous log file
> "$LOG_FILE"

nohup n8n start --tunnel > "$LOG_FILE" 2>&1 &
N8N_PID=$!

echo "[INFO] n8n started with PID: $N8N_PID. Waiting for it to initialize..."

sleep 5 # Give n8n a few seconds to start up

# 5. Verify that n8n is running
if kill -0 $N8N_PID > /dev/null 2>&1; then
  echo "[SUCCESS] n8n is running at http://localhost:$PORT"
  echo "[INFO] Logs are being written to $LOG_FILE"
  echo "[INFO] To stop n8n, run: kill $N8N_PID"
else
  echo "[ERROR] n8n failed to start. Please check the logs for details:"
  echo "--- Last 10 lines of $LOG_FILE ---"
  tail -n 10 "$LOG_FILE"
  echo "---------------------------------"
  exit 1
fi
