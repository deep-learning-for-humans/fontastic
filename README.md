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


## Generate training data

The thought process behind running training and evaluation is to run each off it as an experiment with certain artifacts associated to the experiment. 
This gives us the following benefits:

* Restart experiments at various stagesired rated during the experiment run
* Version control of experiments

Please look at the ```TRAIN_TEST_SPLIT``` section in the ```config.ini``` to understand the configurations required to start an experiment and generate test and train data.

The command to use is : ```python fontastic/data_generation/train_test_split.py --config fontastic/data_generation/config.ini``` 

This will generate an ```experiments folder``` with the ```experiment_id``` as sub folder to store the artifacts. In case the ```experiment_id``` is left empty in the config during the first run, this will be populated and written back to the config. 

You should see a csv for ```train``` and ```test``` respectively in the experiments path folder.