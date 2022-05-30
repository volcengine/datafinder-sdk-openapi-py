rm -rf dist
rm -rf rangersdk.egg-info
python3 setup.py sdist
cp -f dist/rangersdk-1.2.0.tar.gz release/
