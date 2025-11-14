#!/bin/bash

echo "========================================================================"
echo "Verifying Ollama Models in K8s"
echo "========================================================================"
echo ""

# Check init container logs
echo "1. Checking init container logs..."
echo "----------------------------------------------------------------------"
POD_NAME=$(kubectl get pods -n ollama -l app=ollama -o jsonpath='{.items[0].metadata.name}')

if [ -z "$POD_NAME" ]; then
    echo "❌ No Ollama pod found"
    exit 1
fi

echo "Pod: $POD_NAME"
echo ""

# Show init container logs
echo "Init container logs:"
kubectl logs -n ollama $POD_NAME -c init-model --tail=50

echo ""
echo "----------------------------------------------------------------------"
echo "2. Listing models in running pod..."
echo "----------------------------------------------------------------------"

# List models in the running container
kubectl exec -n ollama $POD_NAME -- ollama list

echo ""
echo "----------------------------------------------------------------------"
echo "3. Testing embedding model..."
echo "----------------------------------------------------------------------"

# Test the embedding model
echo "Testing nomic-embed-text..."
kubectl exec -n ollama $POD_NAME -- ollama show nomic-embed-text

echo ""
echo "========================================================================"
echo "Verification Complete!"
echo "========================================================================"
