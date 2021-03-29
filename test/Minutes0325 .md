# 0325

- [x] Learn how to use conda
- [x] Learn how to use pip
## install anaconda
1. download anaconda
2. create a new environment,type this in a terminal
```
conda create -n name pthon=version
```
3. enter the new environment,type this in a terminal
```
conda activate name #windows
```
## install moviepy
1.  type this in a terminal
 ```
 pip install moviepy
 ```
2. to check whether imagemagick exists  
- [windows](https://pypi.org/project/moviepy/) 
We need to edit **moviepy/config_defaults.py** to provide the path to the ImageMagick binary, which is called convert. It should look like this:
```
IMAGEMAGICK_BINARY = "C:\\Program Files\\ImageMagick_VERSION\\convert.exe"
```
