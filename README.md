# MMA3001 – Environmental Sensor Data Interpolation

## Project Overview

This project investigates how missing environmental sensor measurements are able  to be estimated using numericall inteprolation methods. 
The data was selected from the provides "Monash Smart Infrastructure dataset", using measurements from sensor 6012002000326. Four variables havbe been investigated: temperature, humidity, carbon dioxide, and atmospheric pressure.

The aim of this is to comapre linear interpolation and cubic spline interpolation to determine which method is more accurate and more computationally efficient. 

## Dataset
The project uses the enviornmental data forom the Monash Smartt Infrastructure dataset.
The file used for analysis is 5EnvSensor_MayToDec2024_180kRows.csv

To reproducen the analysis, obtain the data set from the Github repo and place the CSV in the same folder as MMA3001_FINAL
The notebook loads this CSV before selecting the sensor and processing the measurements.

## Methods
Two numerica methods have been tested in the process:
- Linear interpolationL This estimates missing measurements using a straight line between known values.
- Cubic spline interpolation: This estimates missing measurements using connected cubic curvbes passing through known values.

To compare the two measurements, known measurements have been deliberately removed and reconstruxcted using both methodologies.

Accuracy was assessed using Mean Absolute Error and Root Mean Squared Error. 

Additional experiments investigated the effects of diffetent amounts of missing data, consecutive sensor outages and computational runtime.

## Results
The results showed that the linear interpolation generally performed a lot bettere than cubic spline for the four enviornmental datasets investigfated. 
Linear interpolation produced a lower preduction error and required less computational runtime. Based on these results, linear interpolation was selected as the preferred method for this dataset.

## Project Files
MMA3001_FINAL.ipynb             Main notebook containing data processing, experiment, graphs and results
interpolation.py                Python functions for the linear and cubic spline interpolations
requirements.txt                Python packages required to run the project
tests/test_interpolation.py     Automated tests used to check the functions in interpolation.py
test_report.txt                 Results of the automated tests
docs/interpolation.html         JTML documentation generated using pdoc

## How to run the projecct
1. Download or clone the github repo
2. Open the project folder in VS code or equivalent
3. Install Python and required packages
4. Place the environmental sensor CSV file in the proejct folder and check that the file path in the notebook looks correct
5. Open MMA3001_FINAL and select a Python kernel
6. Run the notebook cells to reproduce the analysis

In terminal set your file location to the folders location 
Install the required packages using:
python -m pip install -r requirements.txt

Run the automated tests using:
python -m pytest tests -v

Generate the HTML docs usng:
python -m pdoc -o docs interpolation

## Limitations
The analysis foccuses on one environemntal sensor (not all) and four environmental variables. Results may differ from oter sensors or monitoring environments.

Interpolation also relies on measurmeents surrounding the missing data being available. Where there is large gaps and sudden changes in readings this can reduce prediction accuracy.

## AI assistance
ChatGPT was used to assist with writting Python code and development, debugging, documentation and automated testing. The generated material has been reviewed, cehcked using numerical experiments and the automated tests. A more etailed reflection is included in the written project report. 