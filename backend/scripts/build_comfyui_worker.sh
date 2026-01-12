#!/bin/bash
# Build and push ComfyUI worker Docker image for RunPod

set -e

# Configuration
DOCKER_USERNAME="${DOCKER_USERNAME:-your-dockerhub-username}"
IMAGE_NAME="uncensored-comfyui-worker"
VERSION="v1.0"
FULL_IMAGE="${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"

echo "🐳 Building ComfyUI Worker Docker Image..."
echo "   Image: ${FULL_IMAGE}"
echo ""

# Build the image
cd "$(dirname "$0")/../worker"
docker build -f Dockerfile.multi -t ${FULL_IMAGE} .

echo ""
echo "✅ Build complete!"
echo ""
echo "📤 To push to Docker Hub:"
echo "   docker push ${FULL_IMAGE}"
echo ""
echo "📋 To use on RunPod:"
echo "   1. Go to RunPod Console → Templates"
echo "   2. Create new template with image: ${FULL_IMAGE}"
echo "   3. Set container disk: 50GB+ (for models)"
echo "   4. Create endpoint using this template"
echo ""
echo "💡 Tip: Models will be downloaded on first use, or pre-download them in the Dockerfile"
