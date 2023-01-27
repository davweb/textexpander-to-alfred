# textexpander-to-alfred
Python script to convert TextExpander 7 CSV files to Alfred 5 `.alfredsnippets` files

## Introduction
This repository contains a script which convert TextExpander 7 CSV files to Alfred 5 `.alfredsnippets` files.  It only handles the subset of TextExpander tokens that I used in my collections, but could be easily expanded to handle more.

## Installation
1. Check out this repository.
2. Create and source a Python virtual environment:
    `python -m venv --prompt textexpander-to-alfred .venv`
    `source .venv/bin/activate`
3. Install `pip` and `pip-tools`:
    `python -m pip install --upgrade pip pip-tools`
4. Generate the `requirements.txt` file:
    `pip-compile requirements.in`
5. Install the dependencies:
    `pip-sync`

## Running the script
1. Run the script passing the name of the `.csv` file to convert as an argument:
    `python textexpander_to_alfred.py Export.csv`
2. Double-click on the generated `.alfredsnippets` file to import it.
