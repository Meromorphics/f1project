library(cmdstanr)
library(loo)
library(rstan)

year = 2023

csv_folder_path <- sprintf("project/year%d_model_sample_csvs", year)
vector_of_files = list.files(path = csv_folder_path, pattern = "\\.csv$", full.names = TRUE)
fit <- cmdstanr::as_cmdstan_fit(vector_of_files)
fit$loo(cores = 10)

csv_folder2_path <- sprintf("project/year%d_model2_sample_csvs", year)
vector_of_files2 = list.files(path = csv_folder2_path, pattern = "\\.csv$", full.names = TRUE)
fit2 <- cmdstanr::as_cmdstan_fit(vector_of_files2)
fit2$loo(cores = 10)

csv_folder3_path <- sprintf("project/year%d_model3_sample_csvs", year)
vector_of_files3 = list.files(path = csv_folder3_path, pattern = "\\.csv$", full.names = TRUE)
fit3 <- cmdstanr::as_cmdstan_fit(vector_of_files3)
fit3$loo(cores = 10)
