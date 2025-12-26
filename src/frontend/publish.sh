#!/bin/bash

# This script was made to quickly make a production-ready release of the frontend.
# Why not use GitHub Actions? Because this was way faster.

# Remove old files and ready new directories
rm -rf publish
mkdir publish
mkdir publish/pages
mkdir publish/assets

# Start npm build
cd loan-data
npm run build
cd ..

# Move required files to publish for release
mv dist/index.html publish/pages
mv dist/assets/* publish/assets
cp react_server.py publish

# Cleanup
rm -rf dist