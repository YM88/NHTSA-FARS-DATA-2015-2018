# Analysis of aggravating factors for fatal road accidents

National Highway Traffic Safety Administration (NHTSA)<br>
Fatality Analysis Reporting System (FARS)

## Overview

The scope of this project was to predict the fatal traffic accidents that
have more than one fality. Understanding what details of the accidents
contribute to more fatalities, might then contribute to formulating
changes to policies and best practices that would ulimately reduce the
number of fatalities on roads.

## Data

The NHTSA data between 2015 and 2018 has been used. More specifically,
the data corresponding to 2015-2017 was used to train the algorithm, and
the 2018 data was used for testing.

## Methodology

The Random Forest algorithm provided by scikit learn was employed here.
Select features and custom aggregates of select features from the dataset
were utilized for the classification. Exact details are provided in the
accompaning notebooks.

## Results

The classification model did not work very well as implemented here. The
major drawback is that the features employed so far are not predictive.
More time is needed to find better features.

However we found that the latitude and longitude of the accident location
are very rough predictors of accident gravity. Although these features
are not usable, they provide a simple-to-understand threshold for
measuring feature importance. Relative to these we have found that
"involving pedestrians" is a better measure of accident severity.

Other features may be compared in the future and we hope that several
iterations will provide usable features to complete a model analysis.

## Notebooks

The notebooks folder contains all the Jupyter notebooks used for the
current analysis.