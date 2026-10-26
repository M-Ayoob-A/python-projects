#!/bin/bash
set -euo pipefail

echo "Installing OpenCode CLI agent..."
npm install -g opencode-ai

if [ -z "${THAURA_API_KEY:-}" ]; then
  echo "WARNING: THAURA_API_KEY is not set. Add it as a Codespaces secret and rebuild."
fi

echo "Setup complete! Run: opencode"