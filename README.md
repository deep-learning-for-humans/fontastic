# fontastic
Font classifier

This repository contains experiments for classfying fonts from images.
Currently it consists of scrapers to pull the data.

## Installation Instructions

* Requirments 
    * python3
    * pip3
    * virtualenv

* How to install
    * ``` virtualenv -p /usr/bin/python3 venv ```
    * ``` source venv/bin/activate ```
    * ``` pip install -r requirements.txt ``` 
    * ``` export PYTHONPATH=.```


# Working with the Fontastic package

The fontastic package contains the following folder structure:

```
fontastic -- 
            scrape
            utils
```

## How to generate font images?

1. Download [fonts](https://www.dropbox.com/s/tcgh4t2ltttzrrz/fonts-ttfs.tgz?dl=0) and untar it in the location `<project_root>`. So every font will be list as below

	```
	project_root/data/src/fonts/roboto
	project_root/data/src/fonts/roboto/roboto-regular.ttf
	project_root/data/src/fonts/roboto/roboto-bold.ttf
	project_root/data/src/fonts/roboto/roboto-italic.ttf

	project_root/data/src/fonts/open-sans
	project_root/data/src/fonts/open-sans/open-sans-regular.ttf
	project_root/data/src/fonts/open-sans/open-sans-regular.ttf
	project_root/data/src/fonts/open-sans/open-sans-regular.ttf
	...
	...
	...
	```

2. now run ` python fontastic/scrape/local_image_gen.py`
3. the program will create 4k images for every random text and ttf combination. The output image location is `project_root/data/dst/roboto/<output_images>`