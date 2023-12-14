import os
import numpy
import pandas
import cmdstanpy
import arviz

year = 2023

directory = os.path.dirname(os.path.realpath(__file__))

dataframe_file_name = f"f1_data_year{year}.pkl"
saved_dataframe_path = os.path.join(directory, dataframe_file_name)
df = pandas.read_pickle(saved_dataframe_path)

stan_model_exe_name = "model3"
saved_stan_model_path = os.path.join(directory, stan_model_exe_name)
model = cmdstanpy.CmdStanModel(exe_file = saved_stan_model_path)

sample_file_name = f"year{year}_model3_sample_csvs"
saved_sample_model_path = os.path.join(directory, sample_file_name)
sample = cmdstanpy.from_csv(saved_sample_model_path)


data = {"n_drivers": df.index.nunique(),
        "n_races": df["RaceNumber"].nunique(),
        "driver_orderings": df["DriverNumber"].to_numpy(),}


# Now have:
# year: year of races being looked at
# model: cmdstanpy model object, already compiled
# sample: samples from model, already computed

summary_df = sample.summary(percentiles=(5.5, 50, 94.5))

print("Summary statistics:")
print(summary_df)
