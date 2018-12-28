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

### Fetching Data

We fetch the data to train the classification model, we scrape the images from fontsquirrel.com. 
We specify the fonts required in the font section, located in the ``` fontastic/scrape/config.ini ```.
Also provide the number of the parallel process you need and output_dir to store the images for each font in the config section under the respective labels ```multiprocessing_pool_size``` and ```output_dir```

Based on the pool size, we run parallel processes using multiprocessing.
In order to fetch the data, you can call the following script :

```  
python fontastic/scrape/scrape.py --config /<path_to_fontastic_folder>/fontastic/scrape/config.ini
```

You can see that in the ```output_dir``` path specified, you will see a folder for each font in the ```required_fonts``` list provided in the ```config.ini```

