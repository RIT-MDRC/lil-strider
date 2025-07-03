#!/usr/bin/env bash

# If UV is not installed, throw an error
if ! command -v uv &> /dev/null; then
    echo "UV is not installed. Please install UV first."
    exit 1
fi

uv sync
uv pip install RPi.GPIO
