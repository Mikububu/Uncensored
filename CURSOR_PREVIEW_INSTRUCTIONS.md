# How to View Website INSIDE Cursor (Embedded Preview)

## 🎯 Step-by-Step Instructions

### Step 1: Make Sure Server is Running

The server should be running. If not:
- Press `Cmd+Shift+P`
- Type: `Tasks: Run Task`
- Select: `Start Web Server`

### Step 2: Open Simple Browser Panel in Cursor

**This is the key step to view it INSIDE Cursor:**

1. **Press `Cmd+Shift+P`** (Command Palette)
2. **Type exactly:** `Simple Browser: Show`
3. **Press Enter**
4. **A URL bar will appear at the top of the Simple Browser panel**
5. **Type:** `http://localhost:8080`
6. **Press Enter**

The website will now appear **inside Cursor** as a panel!

## 📍 Where to Find Simple Browser

If you don't see "Simple Browser: Show" in the command palette:

### Option A: Check View Menu
1. Click **View** in the menu bar
2. Look for **"Simple Browser"** or **"Show Simple Browser"**
3. Click it, then enter `http://localhost:8080`

### Option B: Install Extension
1. Press `Cmd+Shift+X` (Extensions)
2. Search: **"Simple Browser"**
3. Install if available

### Option C: Use Preview Extension
1. Press `Cmd+Shift+X`
2. Search: **"Live Preview"** or **"Preview"**
3. Install one of these
4. Right-click `frontend/index.html`
5. Select **"Show Preview"**

## 🎨 Alternative: Markdown Preview Style

If Simple Browser isn't available, you can also:

1. **Create a preview HTML file** (I can do this)
2. **Use Cursor's built-in HTML preview**
3. **Or use the Live Server extension**

## ✅ Quick Test

Once you open Simple Browser:
- You should see a panel appear in Cursor
- It will have a URL bar at the top
- Type: `http://localhost:8080`
- The website loads inside that panel!

## 🔧 If It Still Opens External Browser

If it opens in your default browser instead:

1. Check Cursor settings: `Cmd+,`
2. Search for: `browser` or `preview`
3. Look for settings about external vs internal browser
4. Make sure "Simple Browser" is enabled

---

**The key command is: `Simple Browser: Show` from Command Palette!**
