#!/usr/bin/env python3
import sys
import os

print("Python Test Script")
print("==================")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")

try:
    import flask
    print("SUCCESS: Flask imported")
except ImportError:
    print("ERROR: Flask not available")

try:
    import requests
    print("SUCCESS: Requests imported")
except ImportError:
    print("ERROR: Requests not available")

try:
    import psutil
    print("SUCCESS: Psutil imported")
except ImportError:
    print("ERROR: Psutil not available")

print("Python test completed")
