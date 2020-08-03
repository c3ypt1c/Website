# Website
This is my website generation tool that I use on my website. There are still a lot of things to do. Thanks for checking out my repo.

## Installation
The program is very simple to use and install. Essentially it's a bunch of scripts that with some external libraries generate the files to be used on the web. 

### Requirements
1. I developed this on [Python 3.8.4](https://www.python.org/downloads/release/python-384/) but most likely the [latest version](https://www.python.org/downloads/) will work too.
2. [odfpy](https://pypi.org/project/odfpy/) is needed to read the ODF files. Without this, there is nothing to generate. 
3. [datauri](https://pypi.org/project/python-datauri/) is needed to generate the packed downloadable version of the website that contains all of the content embedded in itself. This library is optional. Not installing this library will result in `down.html` not generating. 

#### Installing Python packages
To install the required package, simply invoke pip. You can install the required library using the following commands:

`pip install odfpy`

and the optional library using: 

`pip install python-datauri`


#### Mandatory to do:
 - CSS:
   - Make the page responsive
 - Misc:
   - Create content for the page


#### Optional to do:
 - Generation:
   - Complete down.html
     - Pack CSS images into file for `down.html` automatically.
     - JavaScript LZMA compression. See: https://github.com/LZMA-JS/LZMA-JS
 - Misc:
   - Write about the program in the wiki
