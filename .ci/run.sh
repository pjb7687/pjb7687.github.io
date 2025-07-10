#!/bin/bash
set -x

echo "Getting citations..."
#python3 .ci/get_citations.py

echo "Building website..."
npm run sass
sphinx-build -a source build && touch build/.nojekyll
echo "jeongbinpark.com" > build/CNAME

echo "Setting up Git configuration..."
git config --global user.email "${GIT_EMAIL}"
git config --global user.name "${GIT_NAME}"

echo "Pushing changes to GitHub..."
git add .
git commit -m "Update website"
git push

echo "Website build and push completed successfully."