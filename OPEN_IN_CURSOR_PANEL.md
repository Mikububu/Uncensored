# How to View the Website INSIDE Cursor (Not External Browser)

## ✅ Method 1: Simple Browser Panel (Easiest)

1. **Make sure the server is running:**
   - The server should already be running on port 8080
   - If not, press `Cmd+Shift+P` and type "Tasks: Run Task" → "Start Web Server"

2. **Open Simple Browser inside Cursor:**
   - Press `Cmd+Shift+P` (Command Palette)
   - Type: **`Simple Browser: Show`**
   - Press Enter
   - In the URL bar that appears, type: **`http://localhost:8080`**
   - Press Enter

3. **The website will appear in a panel inside Cursor!**

## ✅ Method 2: Using Command Palette Directly

1. Press `Cmd+Shift+P`
2. Type: **`Simple Browser`**
3. Select **"Simple Browser: Show"**
4. Enter: `http://localhost:8080`

## ✅ Method 3: Keyboard Shortcut (If Available)

Some Cursor versions have a shortcut:
- Try: `Cmd+K` then `V` (might open preview)
- Or check: View → Simple Browser

## ✅ Method 4: Right-Click on index.html

1. Right-click on `frontend/index.html` in the file explorer
2. Look for **"Open Preview"** or **"Show Preview"** option
3. This should open it in a side panel

## If Simple Browser Doesn't Appear

If you don't see "Simple Browser" option:

1. **Install Extension:**
   - Press `Cmd+Shift+X` (Extensions)
   - Search for: **"Simple Browser"**
   - Install it if available

2. **Or Use Preview Extension:**
   - Search for: **"Preview"** extension
   - Install: "Preview" by Microsoft or similar

3. **Alternative - Use Live Preview:**
   - Install "Live Preview" extension
   - Right-click `index.html` → "Show Preview"

## Quick Access

Once you've opened it once, Cursor usually remembers. You can:
- Use the Command Palette again
- Or the Simple Browser should appear in the View menu

## Server Status

To verify server is running:
- Check the terminal panel at the bottom
- You should see: "Server running at http://localhost:8080"
- If not running, start it with the task above

---

**The key is using "Simple Browser: Show" from the Command Palette!**
