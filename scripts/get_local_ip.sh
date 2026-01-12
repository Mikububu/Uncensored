#!/bin/bash

# Quick script to get your local IP address for accessing the app in simulators

IP_ADDRESS=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)

if [ -z "$IP_ADDRESS" ]; then
    echo "❌ Could not find local IP address"
    echo ""
    echo "Try these commands:"
    echo "  ifconfig | grep 'inet ' | grep -v 127.0.0.1"
    echo "  ipconfig getifaddr en0"
    echo "  ipconfig getifaddr en1"
    exit 1
fi

PORT=8080
URL="http://${IP_ADDRESS}:${PORT}"

echo "📍 Your Local IP Address: $IP_ADDRESS"
echo "🌐 App URL: $URL"
echo ""
echo "To access in iPhone Simulator:"
echo "  1. Open Safari in the simulator"
echo "  2. Navigate to: $URL"
echo ""
echo "💡 Remember: Use this IP address, NOT localhost!"
