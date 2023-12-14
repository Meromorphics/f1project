import os
import cmdstanpy

# compile driver_constructor_model.stan
directory = os.path.dirname(os.path.realpath(__file__))
stan_model_file_name = "driver_constructor_model.stan"
saved_stan_model_path = os.path.join(directory, stan_model_file_name)
model = cmdstanpy.CmdStanModel(stan_file = saved_stan_model_path, compile = "force")

# compile driver_constructor_circuit_model.stan
#stan_model2_file_name = "driver_constructor_circuit_model.stan"
#saved_stan_model2_path = os.path.join(directory, stan_model2_file_name)
#model2 = cmdstanpy.CmdStanModel(stan_file = saved_stan_model2_path, compile = "force")

# compile driver_model.stan
stan_model3_file_name = "driver_model.stan"
saved_stan_model3_path = os.path.join(directory, stan_model3_file_name)
model3 = cmdstanpy.CmdStanModel(stan_file = saved_stan_model3_path, compile = "force")
