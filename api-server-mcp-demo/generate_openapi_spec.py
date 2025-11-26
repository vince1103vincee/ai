#!/usr/bin/env python3
"""
Generate OpenAPI spec as YAML file
"""
import json
import yaml
from pathlib import Path
import sys
import requests
import time
import subprocess
import signal
import os

def generate_openapi_spec():
    """Generate OpenAPI spec from Flasgger and save as YAML"""

    # Start Flask server in background
    print("⏳ Starting API server...")
    server_process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Path(__file__).parent
    )

    # Wait for server to start
    time.sleep(3)

    try:
        # Fetch the spec from running server
        print("📥 Fetching OpenAPI spec from server...")
        response = requests.get("http://localhost:8000/apispec_1.json")
        response.raise_for_status()

        spec_dict = response.json()

        # Clean up Swagger 2.0 fields to keep only OpenAPI 3.x
        swagger_2_fields = ['swagger', 'definitions', 'basePath', 'host', 'schemes', 'consumes', 'produces']
        for field in swagger_2_fields:
            if field in spec_dict:
                del spec_dict[field]

        # Reorder keys to OpenAPI 3.x standard order
        ordered_spec = {}
        key_order = ['openapi', 'info', 'servers', 'tags', 'paths', 'components', 'security', 'externalDocs']

        # Add keys in standard order
        for key in key_order:
            if key in spec_dict:
                ordered_spec[key] = spec_dict[key]

        # Add any remaining keys not in standard order
        for key in spec_dict:
            if key not in ordered_spec:
                ordered_spec[key] = spec_dict[key]

        # Save as YAML
        output_file = Path(__file__).parent / "openapi.yaml"

        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(ordered_spec, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        print(f"✅ OpenAPI spec saved to: {output_file}")
        print(f"   File size: {output_file.stat().st_size} bytes")
        print(f"\n📋 Preview (first 50 lines):")
        print("=" * 60)
        with open(output_file, 'r') as f:
            for i, line in enumerate(f):
                if i >= 50:
                    print("   ... (truncated)")
                    break
                print(line.rstrip())

        return output_file

    finally:
        # Kill the server
        print("\n⏹️  Stopping server...")
        os.kill(server_process.pid, signal.SIGTERM)
        server_process.wait()

if __name__ == "__main__":
    generate_openapi_spec()
