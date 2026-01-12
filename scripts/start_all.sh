#!/bin/bash
# Start both ComfyUI and the website

cd "$(dirname "$0")/.."

echo "🚀 Starting Uncensored Studio..."
echo ""

# Start website in background
echo "🌐 Starting website on http://localhost:8080..."
cd frontend
npm start > /tmp/website.log 2>&1 &
WEBSITE_PID=$!
cd ..

# Start ComfyUI in background
echo "🎨 Starting ComfyUI on http://localhost:8188..."
python3 scripts/start_comfyui.py > /tmp/comfyui.log 2>&1 &
COMFYUI_PID=$!

echo ""
echo "✅ Both services started!"
echo ""
echo "📊 Status:"
echo "   Website: http://localhost:8080 (PID: $WEBSITE_PID)"
echo "   ComfyUI: http://localhost:8188 (PID: $COMFYUI_PID)"
echo ""
echo "📝 Logs:"
echo "   Website: tail -f /tmp/website.log"
echo "   ComfyUI: tail -f /tmp/comfyui.log"
echo ""
echo "🛑 To stop:"
echo "   kill $WEBSITE_PID $COMFYUI_PID"
echo ""
echo "⏳ Waiting 3 seconds for services to start..."
sleep 3

# Check if services are running
if curl -s http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ Website is running!"
else
    echo "⚠️  Website may still be starting..."
fi

if curl -s http://localhost:8188 > /dev/null 2>&1; then
    echo "✅ ComfyUI is running!"
else
    echo "⚠️  ComfyUI may still be starting..."
fi

echo ""
echo "🌐 Open http://localhost:8080 in your browser!"
