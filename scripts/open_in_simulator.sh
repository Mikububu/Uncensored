#!/bin/bash

# Script to automatically open the uncensored app in iPhone Simulator

echo "🚀 Opening Uncensored App in iPhone Simulator..."

# Get the local IP address
IP_ADDRESS=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)

if [ -z "$IP_ADDRESS" ]; then
    echo "❌ Could not find local IP address"
    echo "   Please find your IP manually: ifconfig | grep 'inet '"
    exit 1
fi

PORT=8080
URL="http://${IP_ADDRESS}:${PORT}"

echo "📍 Server URL: $URL"
echo ""

# Check if server is running
if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Server doesn't appear to be running on port $PORT"
    echo "   Starting server in background..."
    cd "$(dirname "$0")/../frontend"
    npm start > /dev/null 2>&1 &
    SERVER_PID=$!
    echo "   Server started (PID: $SERVER_PID)"
    echo "   Waiting 3 seconds for server to start..."
    sleep 3
fi

# List available iPhone simulators
echo "📱 Available iPhone Simulators:"
xcrun simctl list devices available | grep -i "iphone" | head -5
echo ""

# Get first available iPhone simulator
DEVICE=$(xcrun simctl list devices available | grep -i "iphone" | head -1 | sed 's/.*(\(.*\))/\1/' | tr -d ' ')

if [ -z "$DEVICE" ]; then
    echo "❌ No iPhone simulators found"
    echo "   Please install Xcode and create a simulator"
    exit 1
fi

echo "🎯 Using device: $DEVICE"

# Boot the simulator if not already booted
if ! xcrun simctl list devices | grep -q "$DEVICE.*Booted"; then
    echo "🔌 Booting simulator..."
    xcrun simctl boot "$DEVICE" 2>/dev/null
    sleep 2
fi

# Open Simulator app
echo "📲 Opening Simulator app..."
open -a Simulator

# Wait a moment for Safari to be ready
sleep 3

# Open URL in Safari
echo "🌐 Opening Safari with URL: $URL"
xcrun simctl openurl booted "$URL"

echo ""
echo "✅ Done! The app should open in Safari on the simulator."
echo ""
echo "💡 Tips:"
echo "   - If Safari doesn't open, manually open Safari in the simulator"
echo "   - Navigate to: $URL"
echo "   - To test on different devices, run: xcrun simctl list devices"
