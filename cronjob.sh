#!/bin/bash

# Activate virtual environment if needed
source ~/newsquest/server/venv/bin/activate

echo "Starting daily automation at $(date)"

# Step 1: Curl the headlines endpoint
echo "Fetching headlines..."
curl -s http://127.0.0.1:5000/headlines
echo "Waiting 1 minute to allow data to settle..."
sleep 60

# Step 2: Run the crossword generator script
echo "Starting crossword generator..."
python3 ~/newsquest/server/app/puzzle/generator.py &

GEN_PID=$!
echo "Generator running with PID $GEN_PID"

# Step 3: Wait at least 15 minutes
echo "Waiting for at least 15 minutes..."
sleep 900

# Step 4: Wait until process completes (if it's still running)
if ps -p $GEN_PID > /dev/null
then
   echo "Generator still running. Waiting for it to finish..."
   wait $GEN_PID
   echo "Generator finished."
else
   echo "Generator completed within 15 minutes."
fi

echo "Daily crossword automation complete at $(date)"
