#!/bin/bash

# List of important files to check
required_files=(
  "frontend/package.json"
  "frontend/tailwind.config.js"
  "frontend/postcss.config.js"
  "backend/requirements.txt"
  "backend/Dockerfile"
  ".github/workflows/docker-build.yml"
)

# Check if all files are present
for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "ERROR: $file is missing!"
    exit 1
  else
    echo "$file exists."
  fi
done

# Check if the frontend/src directory and any files inside it exist
frontend_src_dir="frontend/src"
if [ -d "$frontend_src_dir" ]; then
  echo "$frontend_src_dir directory exists."
  # Optionally, list files in frontend/src directory
  echo "Listing files in $frontend_src_dir:"
  ls -R "$frontend_src_dir"
else
  echo "ERROR: $frontend_src_dir directory is missing!"
  exit 1
fi

# Check if the backend directory exists
if [ ! -d "backend" ]; then
  echo "ERROR: Directory backend is missing!"
  exit 1
else
  echo "Directory backend exists."
fi

echo "All required files are present. Ready to push to GitHub."

exit 0

