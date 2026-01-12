# Opening the Web App in Cursor

## ✅ Server is Running!

The web server is now running on **port 8080**.

## How to Open in Cursor:

### Option 1: Use Cursor's Built-in Browser Preview

1. **Press `Cmd+Shift+P`** (or `Ctrl+Shift+P` on Windows/Linux)
2. Type: **"Simple Browser"** or **"Show Preview"**
3. Select: **"Simple Browser: Show"**
4. Enter URL: `http://localhost:8080`

### Option 2: Use Cursor's Command Palette

1. **Press `Cmd+Shift+P`**
2. Type: **"Open Preview"**
3. Or use: **"View: Show Preview"**
4. Enter: `http://localhost:8080`

### Option 3: Right-Click on index.html

1. Right-click on `frontend/index.html`
2. Select **"Open with Live Server"** (if extension installed)
3. Or **"Reveal in Finder"** then open in browser

### Option 4: Direct Browser Link

Just click or copy this URL:
**http://localhost:8080**

## Quick Access

The app is available at:
- **Local:** http://localhost:8080
- **Network:** http://172.20.10.4:8080 (for iPhone simulators)

## Server Status

To check if server is running:
```bash
lsof -i :8080
```

To stop the server:
```bash
# Find the process
lsof -ti:8080

# Kill it
kill $(lsof -ti:8080)
```

## Cursor Extensions (Optional)

If you want better web preview in Cursor:
- Install "Live Server" extension
- Install "Preview" extension
- Install "Simple Browser" extension

But the built-in Simple Browser should work fine!
