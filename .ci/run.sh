#!/bin/bash
set -x

echo "Getting citations..."
python3 .ci/get_citations.py

echo "Building website..."
npm run sass
sphinx-build -a source build && touch build/.nojekyll
echo "jeongbinpark.com" > build/CNAME

echo "Setting up Git configuration..."
git config --global user.email "${GIT_EMAIL}"
git config --global user.name "${GIT_NAME}"

echo "Pushing cache changes to GitHub..."
git add .ci/gscache.txt .ci/cofirsts_cocorrespondence_cache.txt
git commit -m "Update cache files"
git push origin source

echo "Pushing gh_pages branch to GitHub..."
git worktree add ../gh-pages gh-pages
cp -r build/* ../gh-pages/
cd ../gh-pages
git add .
git commit -m "Update website"
git push origin gh-pages

echo "Website build and push completed successfully."