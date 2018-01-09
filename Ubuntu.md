#Running Inselect on Ubuntu
Ubuntu is not an officially supported platform. Most Inselect functionality (barcode reading being a notable exception) is usable if a number of Python packages are installed. The following instructions have been tested on Ubuntu 16.04 and should work on most recent Ubuntu releases.

### Preparation
```
sudo apt-get install python-pyside python-pathlib python-opencv 
sudo apt-get install python-unicodecsv python-humanize python-psutil python-pip

pip install schematics
```

### Download Inselect
```
git@github.com:NaturalHistoryMuseum/inselect.git
```

### Running Inselect
```
cd inselect
python inselect.py
```
