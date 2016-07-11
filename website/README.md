# Install
```
cd website
mkvirtualenv --python=/Users/lawrence/local/python-3.5.2/bin/python3 inselect-pages
pip install -r requirements.pip
git clone git@github.com:quicklizard99/pelican-themes.git ../../pelican-themes/
```

# Dev
Edit `pelicanconf.py` and set `SITEURL=''`.

```
rm -rf output && make html
./develop_server.sh start
```

Open http://localhost:8000.

```
# When finished
./develop_server.sh stop
```

# Theme
Documentation for the
[pelican-bootstrap3](https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3).


# Release
Edit `pelicanconf.py` and set `SITEURL=''`.

```
rm -rf output && make html
ghp-import output
git push origin gh-pages
```
