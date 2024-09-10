# simple-scrape
In-construction light program to scrape numeric data. Currently specific to [Selected Unemployment Indicators by Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/release/tables?rid=50&eid=3029&od=#)
## Function
Scrape numeric data from websites. Future versions will be non-site-specific, and employ Large Language Models to detect which types of tags comprise desired data. 
## Installation
If using conda, install dependencies with:
```
conda env create --name envname --file=environment.yml
```
If using pip, install dependencies with:
```
pip install -r requirements.txt
```
## Usage
Run program with ```python3 scraper.py```. After user input for desired section of data, output will be: 
1. ```target_url.html``` containing retrieved HTML
2. Pop-up window displaying data
3. ```figure.png``` displaying same figure in pop-up window
