import os

def getenv(name, required=True):
    """Get environment variable or raise runtime error with message."""
    value = os.getenv(name)
    if not value and required:
        raise RuntimeError(f"Environment variable '{name}' not found.")
    return value
