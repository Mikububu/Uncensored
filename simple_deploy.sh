#!/bin/bash
# Simple deployment script

echo "🚀 Simple Deployment Script"
echo ""

# Check API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ ERROR: OPENROUTER_API_KEY not set"
    echo "Set it with: export OPENROUTER_API_KEY='sk-or-v1-...'"
    exit 1
fi

echo "✅ OpenRouter API key found: ${OPENROUTER_API_KEY:0:15}...${OPENROUTER_API_KEY: -4}"

# Test the simple worker
echo ""
echo "🧪 Testing simple worker..."
cd /Users/michaelperinwogenburg/Desktop/big\ challenge/Uncensored
python3 backend/simple_worker.py

# Deploy to Netlify
echo ""
echo "🌐 Deploying to Netlify..."
NETLIFY_AUTH_TOKEN='nfp_qubuGtQyMZ8QxwPhxbAT2EcsgpdxLY7Qd4ba' netlify deploy --site=6a1b10fb-a8b1-4ca9-9c5b-f812e5c65e50 --prod --dir=. --timeout=90 2>&1

echo ""
echo "✅ Deployment complete!"
echo "   https://aprils-spielzeugkasten.netlify.app/"