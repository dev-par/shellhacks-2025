#!/bin/bash
# Simple script to clean up ports

echo "🧹 Cleaning up ports..."

# Kill processes on common ports
for port in 8000 8001 8002 8003 3000; do
    echo "Checking port $port..."
    PID=$(lsof -ti :$port 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "Killing process $PID on port $port"
        kill -9 $PID 2>/dev/null
    else
        echo "Port $port is free"
    fi
done

echo "✅ Cleanup complete!"
