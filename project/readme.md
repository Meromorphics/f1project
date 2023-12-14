# Code for the essay "Predicting Formula One race results using a rank ordered logit model"
John Walker

sta221 (UC Davis) class project

# Code files
Stan files:

1. driver_model.stan
2. driver_constructor_model.stan
3. driver_constructor_circuit_model.stan

R files:

1. perform_loo.R

Python files:

1. compile_models.py
2. get_data.py
3. sample_models.py
4. analyze_samples_driver_model.py
5. analyze_samples_driver_constructor_model.py
6. analyze_samples_driver_constructor_circuit_model.py
7. posterior_predictive_inference.py

# Description of code files
Stan files are designed to sample their described model's posterior distributions. They are not meant to be ran directly, rather called to be compiled from Python and told to run from Python (R and some other languages can also be used, this project uses Python).

The R file is meant to do a statistical analysis that could not be done using Python (the Arviz function, a Python library, that translates Python-Stan data to Arviz data was bugged at the time of writing; so instead the R equivalent was used). Namely, "efficient leave one out cross validation" (called loo). 3 models are written in this code, the purpose of this file is to decide which model best fits (has the best cross validation results).

The Python files do the heavy lifting and main analysis.
They are roughly written in order of use.

compile_models.py should be called first, since it compiles the three stan files.

Next, get_data.py should be ran to store race result data in a dataframe to be used in other code files.
To do this, change the year variable near the top of the file to the desired year of results, and n variable to the number of races done in that year.
Saves the resulting pandas dataframe as "f1_data_year{year}.pkl" where {year} is the input year (for example, 2023).
Resulting dataframe should have no errors, but may due to the fastf1 Python library where the data was obtained from.
For example, hardcoded into get_data.py is a pair of lines that changes the index of one row of the dataframe since fastf1 loads the driver name as NaN but referencing actual results manually finds that this index belongs to the driver Stroll (STR in the code).

The files analyze_samples_driver_model.py, analyze_samples_driver_constructor_model.py, and analyze_samples_driver_constructor_circuit_model.py are setup to allow for easy access to sample results (and original data results) for analysis. They are designed to be ran in either interactive mode or appended on.
The file analyze_samples_driver_constructor_model.py contains appended code that was used to generate figures and results used in the main essay since this was the model chosen for the essay.

The file posterior_predictive_inference.py performs "visual posterior predictive inference" on the driver_constructor_model.stan samples.
Again, the driver_constructor_model was chosen for this since it was the model chosen for the essay.
This visual posterior predictive inference consists of simulating races obtained from the sample data, and comparing the finishing position frequency of a given driver to their actual finishing position frequency in a given year, by display of a histogram.
If the simulated data and actual data agree (both generated histograms look roughly similar), then the check succeeds.