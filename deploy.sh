#!/bin/bash
# Deployment script for Uncensored Studio

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Uncensored Studio Deployment${NC}\n"

# Check for required tools
command -v git >/dev/null 2>&1 || { echo -e "${RED}Git is required but not installed.${NC}" >&2; exit 1; }
command -v netlify >/dev/null 2>&1 || { echo -e "${YELLOW}Netlify CLI not found, using curl...${NC}" ; USE_CURL=true; }

# Check for API keys
if [ -z "$NETLIFY_AUTH_TOKEN" ]; then
    if [ -f .env ]; then
        source .env
    fi
fi

if [ -z "$NETLIFY_AUTH_TOKEN" ]; then
    echo -e "${RED}❌ NETLIFY_AUTH_TOKEN not set${NC}"
    echo "Export it or add to .env file:"
    echo "  export NETLIFY_AUTH_TOKEN='nfp_...'"
    exit 1
fi

echo -e "${GREEN}✓ Netlify token found${NC}"

# Get site ID
SITE_ID="6a1b10fb-a8b1-4ca9-9c5b-f812e5c65e50"

# Stage and commit changes
echo -e "\n${YELLOW}📦 Committing changes...${NC}"
git add -A 2>/dev/null || true
COMMIT_MSG="${1:-$(date '+%Y-%m-%d %H:%M')}"
git commit -m "$COMMIT_MSG" 2>/dev/null && echo -e "${GREEN}✓ Committed${NC}" || echo -e "${YELLOW}✓ Nothing to commit${NC}"

# Push to GitHub
echo -e "\n${YELLOW}📤 Pushing to GitHub...${NC}"
git push origin main 2>/dev/null || echo -e "${YELLOW}✓ Already up to date${NC}"

# Deploy to Netlify
echo -e "\n${YELLOW}🌐 Deploying to Netlify...${NC}"
if [ "$USE_CURL" = true ]; then
    response=$(curl -s -X POST \
        -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"files":[]}' \
        "https://api.netlify.com/sites/$SITE_ID/deploys" 2>&1)
    
    if echo "$response" | grep -q "error"; then
        echo -e "${RED}Deploy failed: $response${NC}"
        exit 1
    fi
    deploy_id=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}✓ Deploy triggered (ID: $deploy_id)${NC}"
else
    netlify deploy --site="$SITE_ID" --prod --dir=frontend --timeout=120 2>&1
fi

echo -e "\n${GREEN}✅ Deployment complete!${NC}"
echo "   https://aprils-spielzeugkasten.netlify.app/"
