# Fix: Accidentally Declined Localhost Permission

If you accidentally clicked "Deny" or "Block" on a localhost permission pop-up, here's how to fix it:

## Method 1: Reset Cursor Settings (Easiest)

1. **Close Cursor completely**
2. **Open Terminal and run:**
```bash
# This will reset Cursor's security settings
defaults delete com.todesktop.230313mzl4w4u92 2>/dev/null
# Or try:
rm -rf ~/Library/Application\ Support/Cursor/User/workspaceStorage/*
```

3. **Reopen Cursor**
4. **Try Simple Browser again** - the pop-up should reappear
5. **Click "Allow" this time**

## Method 2: Reset via Cursor Settings

1. Press `Cmd+,` (Settings)
2. Search for: `security` or `localhost` or `browser`
3. Look for settings like:
   - "Security: Allowed Origins"
   - "Simple Browser: Allowed URLs"
   - "Preview: Allowed Hosts"
4. Add `http://localhost:8080` to the allowed list

## Method 3: Trigger the Pop-up Again

1. **Close and reopen Cursor**
2. **Try to open Simple Browser:**
   - `Cmd+Shift+P` → `Simple Browser: Show`
   - Enter: `http://localhost:8080`
3. **The permission pop-up should appear again**
4. **Click "Allow" or "Yes"**

## Method 4: Manual Permission Reset

1. **Quit Cursor completely** (Cmd+Q)
2. **Open Terminal:**
```bash
# Find Cursor's config directory
cd ~/Library/Application\ Support/Cursor

# Look for security/permission files
find . -name "*security*" -o -name "*permission*" -o -name "*localhost*"
```

3. **Delete or modify those files**
4. **Reopen Cursor**

## Method 5: Use Different Port (Workaround)

If you can't reset the permission, change the port:

1. Edit `frontend/server.js`
2. Change port from `8080` to `8081`:
```javascript
const port = process.env.PORT || 8081;
```

3. Restart server
4. Use `http://localhost:8081` in Simple Browser
5. New port = new permission request!

## Quick Test

After trying any method above:

1. Press `Cmd+Shift+P`
2. Type: `Simple Browser: Show`
3. Enter: `http://localhost:8080`
4. **If pop-up appears, click "Allow"!**

---

**Most likely solution: Just restart Cursor and try again - the pop-up should reappear!**
