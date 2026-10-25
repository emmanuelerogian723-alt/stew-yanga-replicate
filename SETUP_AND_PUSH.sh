#!/bin/bash
# Run this inside GitHub Codespaces (or any machine with Docker).
set -e
pip install cog
cog login --token "$REPLICATE_API_TOKEN"
cog push emmanuelerogian723-alt/stew-yanga
echo "LIVE! https://replicate.com/emmanuelerogian723-alt/stew-yanga"
