#!/bin/bash
# Start ComfyUI and open it in Cursor's Simple Browser

cd "$(dirname "$0")/../comfyui"

echo "🎨 Starting ComfyUI..."
echo "📍 Will open in Cursor browser at http://localhost:8188"
echo ""

# Start ComfyUI in background
python3 main.py --listen 0.0.0.0 --port 8188 > /tmp/comfyui.log 2>&1 &
COMFYUI_PID=$!

echo "✅ ComfyUI started (PID: $COMFYUI_PID)"
echo "📝 Logs: tail -f /tmp/comfyui.log"
echo ""
echo "⏳ Waiting for ComfyUI to be ready..."

# Wait for ComfyUI to be ready
for i in {1..30}; do
    if curl -s http://localhost:8188 > /dev/null 2>&1; then
        echo "✅ ComfyUI is ready!"
        echo ""
        echo "🌐 Opening in Cursor..."
        echo "   URL: http://localhost:8188"
        echo ""
        echo "💡 To stop ComfyUI, run: kill $COMFYUI_PID"
        echo ""
        
        # Try to open in Cursor's Simple Browser
        # Note: Cursor will need to be configured to allow localhost
        open "http://localhost:8188" 2>/dev/null || echo "⚠️  Could not auto-open. Please open http://localhost:8188 manually"
        
        exit 0
    fi
    sleep 1
done

echo "❌ ComfyUI did not start in time"
kill $COMFYUI_PID 2>/dev/null
exit 1
