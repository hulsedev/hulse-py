if [ -d "dist" ]; then
    rm -rf dist
fi
python3 -m build
twine upload dist/*