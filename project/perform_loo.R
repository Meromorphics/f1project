library(cmdstanr)
library(loo)
library(rstan)

year = 2023

# perform loo on driver_constructor_model
csv_folder_path <- sprintf("project/year%d_driver_constructor_model_sample_csvs", year)
vector_of_files = list.files(path = csv_folder_path, pattern = "\\.csv$", full.names = TRUE)
fit <- cmdstanr::as_cmdstan_fit(vector_of_files)
fit$loo(cores = 10)

# perform loo on driver_constructor_circuit_model
#csv_folder2_path <- sprintf("project/year%d_driver_constructor_circuit_model_sample_csvs", year)
#vector_of_files2 = list.files(path = csv_folder2_path, pattern = "\\.csv$", full.names = TRUE)
#fit2 <- cmdstanr::as_cmdstan_fit(vector_of_files2)
#fit2$loo(cores = 10)

# perform loo on driver_model
csv_folder3_path <- sprintf("project/year%d_driver_sample_csvs", year)
vector_of_files3 = list.files(path = csv_folder3_path, pattern = "\\.csv$", full.names = TRUE)
fit3 <- cmdstanr::as_cmdstan_fit(vector_of_files3)
fit3$loo(cores = 10)
