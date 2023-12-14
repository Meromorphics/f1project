import os
import pandas
import cmdstanpy

year = 2021

# set directory and get data
directory = os.path.dirname(os.path.realpath(__file__))
dataframe_file_name = f"f1_data_year{year}.pkl"
saved_dataframe_path = os.path.join(directory, dataframe_file_name)
df = pandas.read_pickle(saved_dataframe_path)

# sample driver_constructor_model.stan
stan_model_exe_name = "driver_constructor_model"
saved_stan_model_path = os.path.join(directory, stan_model_exe_name)
model = cmdstanpy.CmdStanModel(exe_file = saved_stan_model_path)

data = {"n_drivers": df.index.nunique(),
        "n_constructors": df["TeamNumber"].nunique(),
        "n_races": df["RaceNumber"].nunique(),
        "driver_orderings": df["DriverNumber"].to_numpy(),
        "constructor_orderings": df["TeamNumber"].to_numpy()}

sample_file_name = f"year{year}_driver_constructor_model_sample"
saved_sample_model_path = os.path.join(directory, sample_file_name)

fit = model.sample(data = data,
             chains = 4,
             parallel_chains= 4,
             iter_warmup = 1000,
             iter_sampling = 2000,
             output_dir = saved_sample_model_path)

output_csv_folder_name = f"year{year}_driver_constructor_model_sample_csvs"
output_csv_folder_path = os.path.join(directory, output_csv_folder_name)
fit.save_csvfiles(dir = output_csv_folder_path)




# sample driver_constructor_circuit_model.stan
#stan_model2_exe_name = "driver_constructor_circuit_model"
#saved_stan_model2_path = os.path.join(directory, stan_model2_exe_name)
#model2 = cmdstanpy.CmdStanModel(exe_file = saved_stan_model2_path)

#data2 = {"n_drivers": df.index.nunique(),
#        "n_constructors": df["TeamNumber"].nunique(),
#        "n_races": df["RaceNumber"].nunique(),
#        "driver_orderings": df["DriverNumber"].to_numpy(),
#        "constructor_orderings": df["TeamNumber"].to_numpy(),
#        "race_types": df[["RaceNumber", "CircuitTypeIndex"]].drop_duplicates()["CircuitTypeIndex"].to_numpy()}

#sample_file2_name = f"year{year}_driver_constructor_circuit_model_sample"
#saved_sample_model2_path = os.path.join(directory, sample_file2_name)

#fit2 = model2.sample(data = data2,
#             chains = 4,
#             parallel_chains= 4,
#             iter_warmup = 1000,
#             iter_sampling = 2000,
#             output_dir = saved_sample_model2_path)

#output_csv_folder2_name = f"year{year}_driver_constructor_circuit_model_sample_csvs"
#output_csv_folder2_path = os.path.join(directory, output_csv_folder2_name)
#fit2.save_csvfiles(dir = output_csv_folder2_path)




# sample driver_model.stan
stan_model3_exe_name = "driver_model"
saved_stan_model3_path = os.path.join(directory, stan_model3_exe_name)
model3 = cmdstanpy.CmdStanModel(exe_file = saved_stan_model3_path)


data3 = {"n_drivers": df.index.nunique(),
        "n_races": df["RaceNumber"].nunique(),
        "driver_orderings": df["DriverNumber"].to_numpy(),}

sample_file3_name = f"year{year}_driver_model_sample"
saved_sample_model3_path = os.path.join(directory, sample_file3_name)

fit3 = model3.sample(data = data3,
             chains = 4,
             parallel_chains= 4,
             iter_warmup = 1000,
             iter_sampling = 2000,
             output_dir = saved_sample_model3_path)

output_csv_folder3_name = f"year{year}_driver_model_sample_csvs"
output_csv_folder3_path = os.path.join(directory, output_csv_folder3_name)
fit3.save_csvfiles(dir = output_csv_folder3_path)
