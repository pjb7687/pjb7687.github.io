#!/bin/bash
set -x

echo "Getting citations..."
uv run .ci/get_citations.py

echo "Building website..."
npm run sass
uv run sphinx-build -a source build && touch build/.nojekyll
echo "jeongbinpark.com" > build/CNAME

echo "Setting up Git configuration..."
git config --global user.email "jeongbin.park@pusan.ac.kr"
git config --global user.name "Jeongbin Park"

echo "Pushing cache changes to GitHub..."
git add .ci/gscache.txt .ci/cofirsts_cocorrespondence_cache.txt
git commit -m "Update cache files"
git push origin source

echo "Pushing gh_pages branch to GitHub..."
git worktree add ../gh-pages gh-pages
cp -r build/* ../gh-pages/

pushd ../gh-pages
git add .
git commit -m "Update website"
git push origin gh-pages
popd

echo "Website build and push completed successfully."
