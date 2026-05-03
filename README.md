![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![OSINT](https://img.shields.io/badge/OSINT-Tool-red.svg)
![License](https://img.shields.io/badge/License-Educational-yellow.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Disclaimer : 
This tool is for educational and authorized security testing purposes only.
Only analyze images you own or have permission to investigate. Respect privacy laws in your jurisdiction.
**WHAT YOU DO WITH THIS TOOL IS NOT MY RESPONSIBILITY**

## License : 
This project is for educational purposes as part of mys portfolio.


## What it does : 
takes an image you provide and extracts the metadata it contains, saves it into a json file and also gives you the google maps link using the gps fields.

## Pre-Requisites : 
Python 3.7 + 
pip commands 
internet connection

## Installation :
git clone https://github.com/Madnes-Madlaki/OSINT_Exif_Tool

cd OSINT_Exif_Tool

pip install flask exif requests

python ui.py

then just ctrl+right_click the local host

## CLI Mode : 
python extractScript.py your_PATH_to_the_image.EXTENSION

## Supported formats : 
JPEG (.jpg, .jpeg)
PNG (.png)
GIF (.gif)
BMP (.bmp)
TIFF (.tiff)
