#!/bin/bash
set -e
if [ -z "$REPLICATE_API_TOKEN" ]; then
  echo "Paste your Replicate token (starts with r8_) then press Enter:"
  read -s REPLICATE_API_TOKEN
  export REPLICATE_API_TOKEN
fi
pip install -q cog
cog login --token "$REPLICATE_API_TOKEN"
cog push emmanuelerogian723-alt/stew-yanga
echo ""
echo "LIVE at https://replicate.com/emmanuelerogian723-alt/stew-yanga"
