# Fix: Simple Browser Not Showing in This Cursor Window

Since you can see it in another Cursor window, this might be a workspace-specific issue.

## Quick Fixes to Try:

### 1. Reload Cursor Window
- Press `Cmd+Shift+P`
- Type: `Developer: Reload Window`
- Press Enter
- Then try `Simple Browser: Show` again

### 2. Check if Extension is Disabled for This Workspace
- Press `Cmd+Shift+X` (Extensions)
- Look for "Simple Browser" or "Live Preview"
- Check if it says "Disabled (Workspace)" - if so, click "Enable (Workspace)"

### 3. Use the Other Window Method
Since it works in your other Cursor window:
- Copy the URL: `http://localhost:8080`
- Go to your other Cursor window
- Open Simple Browser there
- Paste the URL

### 4. Install Live Preview Extension (Alternative)
1. Press `Cmd+Shift+X`
2. Search: **"Live Preview"** by Microsoft
3. Install it
4. Right-click on `frontend/index.html`
5. Select **"Show Preview"**

### 5. Check Workspace Settings
The `.vscode/settings.json` file might have something blocking it. I've updated it - try reloading the window.

### 6. Use Command Line to Open
If nothing else works, you can:
- Keep the server running here
- Use the Simple Browser in your other Cursor window
- Or I can create a simple HTML file that opens automatically

## Why This Might Happen:

- Workspace-specific extension settings
- Different Cursor version/update
- Extension disabled for this workspace
- Cache issue

## Quick Workaround:

Since your other window works:
1. Keep this window for coding
2. Use the other Cursor window for preview
3. Both can connect to the same server on `localhost:8080`

Let me know if reloading the window fixes it!
