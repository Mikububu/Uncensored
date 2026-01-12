# Running the Uncensored App on iPhone Simulators

This is a **web app** (HTML/JavaScript), so you can access it in iPhone simulators using Safari.

## Quick Start

### Option 1: Automatic Setup (Recommended)

```bash
# Start the frontend server
cd frontend
npm start

# In another terminal, run the simulator helper
cd ..
./scripts/open_in_simulator.sh
```

### Option 2: Manual Setup

1. **Start the frontend server:**
```bash
cd frontend
npm start
```
Server will run on `http://localhost:8080`

2. **Get your Mac's local IP address:**
```bash
ipconfig getifaddr en0
# or
ifconfig | grep "inet " | grep -v 127.0.0.1
```

3. **Open Safari in iPhone Simulator:**
   - Open Xcode Simulator (or use `xcrun simctl boot <device-id>`)
   - Open Safari in the simulator
   - Navigate to: `http://YOUR_IP_ADDRESS:8080`
   - Example: `http://192.168.1.100:8080`

## Running Multiple iPhone Simulators

### List Available Simulators

```bash
xcrun simctl list devices available
```

### Boot Multiple Simulators

```bash
# Boot iPhone 15 Pro
xcrun simctl boot "iPhone 15 Pro"

# Boot iPhone 14
xcrun simctl boot "iPhone 14"

# Boot iPhone SE
xcrun simctl boot "iPhone SE (3rd generation)"
```

### Open Simulator App

```bash
# Open Simulator app (shows all booted devices)
open -a Simulator
```

### Open URL in Specific Simulator

```bash
# Get device UDID first
xcrun simctl list devices | grep "iPhone 15 Pro"

# Open URL in that device
xcrun simctl openurl <DEVICE_UDID> "http://192.168.1.100:8080"
```

## Quick Scripts

I've created helper scripts (see `scripts/` folder):
- `open_in_simulator.sh` - Automatically opens the app in a simulator
- `start_multiple_simulators.sh` - Boots multiple simulators at once

## Important Notes

### Use Your Mac's IP Address (Not localhost)

- ❌ `http://localhost:8080` - Won't work in simulator
- ✅ `http://192.168.1.100:8080` - Use your Mac's actual IP

The simulator treats `localhost` as the simulator itself, not your Mac.

### Finding Your IP Address

```bash
# Quick command to get your IP
ipconfig getifaddr en0 || ipconfig getifaddr en1
```

Or check System Settings > Network

### Firewall

Make sure your Mac's firewall allows connections on port 8080, or temporarily disable it for testing.

## Testing on Multiple Devices

1. **Start the server:**
```bash
cd frontend
npm start
```

2. **Boot multiple simulators:**
```bash
xcrun simctl boot "iPhone 15 Pro"
xcrun simctl boot "iPhone 14"
xcrun simctl boot "iPhone SE (3rd generation)"
open -a Simulator
```

3. **Get your IP:**
```bash
MY_IP=$(ipconfig getifaddr en0)
echo "Open in Safari: http://$MY_IP:8080"
```

4. **Open in each simulator:**
   - Click on each simulator window
   - Open Safari
   - Navigate to `http://YOUR_IP:8080`

## Creating a Native iOS App (Optional)

If you want a native iOS app instead of using Safari:

1. Create a new Xcode project (iOS App)
2. Use WKWebView to load the web app
3. Configure it to load `http://YOUR_IP:8080`

I can create a simple iOS wrapper app if you want - just let me know!

## Troubleshooting

**Can't connect from simulator:**
- Make sure you're using your Mac's IP, not `localhost`
- Check that the server is running: `lsof -i :8080`
- Try disabling firewall temporarily

**Multiple simulators:**
- Each simulator runs independently
- You can test the same app on different screen sizes
- All simulators can connect to the same server

**Port already in use:**
```bash
# Change port in frontend/server.js
const port = process.env.PORT || 8081
```
