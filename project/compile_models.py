import os
import cmdstanpy

directory = os.path.dirname(os.path.realpath(__file__))
stan_model_file_name = "model.stan"
saved_stan_model_path = os.path.join(directory, stan_model_file_name)
model = cmdstanpy.CmdStanModel(stan_file = saved_stan_model_path, compile = "force")

#stan_model2_file_name = "model2.stan"
#saved_stan_model2_path = os.path.join(directory, stan_model2_file_name)
#model2 = cmdstanpy.CmdStanModel(stan_file = saved_stan_model2_path, compile = "force")

stan_model3_file_name = "model3.stan"
saved_stan_model3_path = os.path.join(directory, stan_model3_file_name)
model3 = cmdstanpy.CmdStanModel(stan_file = saved_stan_model3_path, compile = "force")
