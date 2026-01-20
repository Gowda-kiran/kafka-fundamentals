"""
Schema Registration Script
--------------------------
This script registers Avro schemas to Schema Registry.
In real projects, this runs in CI/CD pipeline after PR merge.

Usage:
    python scripts/register_schemas.py
"""

import json
import requests
import os
from pathlib import Path

SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8881")

# Map schema files to subject names
# Using record_name_strategy: subject = namespace.name
SCHEMA_MAPPINGS = [
    {
        "file": "schemas/orders/order-v1.avsc",
        "subject": "com.orders.Order"  # namespace.name from schema
    }
]

def load_schema(file_path):
    """Load schema from .avsc file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def register_schema(subject, schema):
    """Register schema to Schema Registry"""
    url = f"{SCHEMA_REGISTRY_URL}/subjects/{subject}/versions"
    headers = {"Content-Type": "application/vnd.schemaregistry.v1+json"}

    # Schema must be sent as escaped JSON string
    payload = {"schema": json.dumps(schema)}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        schema_id = response.json().get("id")
        print(f"[OK] Registered '{subject}' with schema ID: {schema_id}")
        return True
    elif response.status_code == 409:
        print(f"[SKIP] Schema '{subject}' already exists (no changes)")
        return True
    else:
        print(f"[FAIL] Failed to register '{subject}': {response.text}")
        return False

def check_compatibility(subject, schema):
    """Check if schema is compatible with existing versions"""
    url = f"{SCHEMA_REGISTRY_URL}/compatibility/subjects/{subject}/versions/latest"
    headers = {"Content-Type": "application/vnd.schemaregistry.v1+json"}
    payload = {"schema": json.dumps(schema)}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        is_compatible = response.json().get("is_compatible", False)
        return is_compatible
    elif response.status_code == 404:
        # No existing schema, so compatible by default
        return True
    else:
        print(f"[WARN] Compatibility check failed: {response.text}")
        return False

def main():
    print("=" * 50)
    print("Schema Registration Script")
    print(f"Registry: {SCHEMA_REGISTRY_URL}")
    print("=" * 50)

    # Get project root
    project_root = Path(__file__).parent.parent

    success_count = 0
    fail_count = 0

    for mapping in SCHEMA_MAPPINGS:
        schema_file = project_root / mapping["file"]
        subject = mapping["subject"]

        print(f"\nProcessing: {mapping['file']}")
        print(f"Subject: {subject}")

        if not schema_file.exists():
            print(f"[FAIL] Schema file not found: {schema_file}")
            fail_count += 1
            continue

        schema = load_schema(schema_file)

        # Check compatibility first
        if check_compatibility(subject, schema):
            print("[OK] Schema is compatible")
            if register_schema(subject, schema):
                success_count += 1
            else:
                fail_count += 1
        else:
            print("[FAIL] Schema is NOT compatible with existing version!")
            fail_count += 1

    print("\n" + "=" * 50)
    print(f"Results: {success_count} succeeded, {fail_count} failed")
    print("=" * 50)

    # Exit with error code if any failed (useful for CI/CD)
    exit(0 if fail_count == 0 else 1)

if __name__ == "__main__":
    main()
