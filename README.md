# St. Louis 2022 Redistricting Project

This repository contains files relevant to a project that explored redistricting methods for St. Louis's 2022 redistricting efforts. 

## Website

Most of the files in this repository are files used to generate a website that showcases the project. To view this website (hosted on Github), click [HERE](https://austintolani.github.io/stlRedistricting/). 

All of the JavaScript used to generate the web maps and page logic found in `results.html` can be found at `assets/js/maps.js`. 

## Python Script to Evaluate Ward Boundaries

As a part of this project, I created a python script that will evaluate potential ward boundaries based on redistricting criteria. This script can be found at `Evaluator.py`. To run this script, first adjust any environmental variables in the scripts based on your workspace and the files you are using. Then, the script can be run from the command line using the following arguments:

```
py Evaluator.py {ward boundaries shapefile} {ward name fields}
```

The following is an example input/output:

```
$ py -2 Evaluator.py Trial5.shp DIST_ID
Progress: 100%|██████████| 100/100 [00:25<00:00,  3.96it/s]

 POPULATION: Equal population criteria satisfied with an overal range of 0.029235820627.
COMPACTNESS: Average Polsby-Popper test value is 0.505516730222.
COHESION:
         Average census block group splits is 1.0.
         Average neighborhood splits is 1.16666666667.
         Average park splits is 1.05172413793.
MINORITY CRITERIA
         Minority criteria (6 wards) satisfied at 40%: True.
         Minority criteria (6 wards) satisfied at 45%: True.
         Minority criteria (6 wards) satisfied at 50%: True.
         Minority criteria (6 wards) satisfied at 55%: False.
         Minority criteria (7 wards) satisfied at 40%: True.
         Minority criteria (7 wards) satisfied at 45%: True.
         Minority criteria (7 wards) satisfied at 50%: False.
         Minority criteria (7 wards) satisfied at 55%: False.
```

## BARD Source Code

Part of this project involved using Better Automated Redistricting (BARD), a software package installed using R. `generateWards.R` is the code used to generate ward boundaries using BARD. 