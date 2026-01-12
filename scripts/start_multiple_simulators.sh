#!/bin/bash

# Script to boot multiple iPhone simulators for testing

echo "📱 Starting Multiple iPhone Simulators..."
echo ""

# Common iPhone simulators to boot
DEVICES=(
    "iPhone 15 Pro"
    "iPhone 14"
    "iPhone SE (3rd generation)"
)

# List all available devices
echo "Available iPhone Simulators:"
xcrun simctl list devices available | grep -i "iphone" | head -10
echo ""

# Boot each device
BOOTED_DEVICES=()

for device in "${DEVICES[@]}"; do
    # Check if device exists
    if xcrun simctl list devices available | grep -q "$device"; then
        echo "🔌 Booting: $device"
        xcrun simctl boot "$device" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            BOOTED_DEVICES+=("$device")
            echo "   ✅ Booted successfully"
        else
            echo "   ⚠️  Already booted or error"
        fi
    else
        echo "   ⏭️  Device not available: $device"
    fi
    echo ""
done

# Open Simulator app to show all booted devices
if [ ${#BOOTED_DEVICES[@]} -gt 0 ]; then
    echo "📲 Opening Simulator app..."
    open -a Simulator
    
    echo ""
    echo "✅ Booted ${#BOOTED_DEVICES[@]} simulator(s):"
    for device in "${BOOTED_DEVICES[@]}"; do
        echo "   - $device"
    done
    
    # Get IP address for easy access
    IP_ADDRESS=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)
    if [ ! -z "$IP_ADDRESS" ]; then
        echo ""
        echo "🌐 To access the app, open Safari in each simulator and navigate to:"
        echo "   http://${IP_ADDRESS}:8080"
    fi
else
    echo "⚠️  No simulators were booted"
fi

echo ""
echo "💡 To boot a specific device manually:"
echo "   xcrun simctl boot 'iPhone 15 Pro'"
echo ""
echo "💡 To list all devices:"
echo "   xcrun simctl list devices"
