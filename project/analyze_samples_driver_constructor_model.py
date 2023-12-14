import os
import numpy
import pandas
import cmdstanpy
import arviz
import matplotlib.pyplot
import matplotlib

matplotlib.rcParams["figure.dpi"] = 200

year = 2021

directory = os.path.dirname(os.path.realpath(__file__))

dataframe_file_name = f"f1_data_year{year}.pkl"
saved_dataframe_path = os.path.join(directory, dataframe_file_name)
df = pandas.read_pickle(saved_dataframe_path)

stan_model_exe_name = "model"
saved_stan_model_path = os.path.join(directory, stan_model_exe_name)
model = cmdstanpy.CmdStanModel(exe_file = saved_stan_model_path)

sample_file_name = f"year{year}_model_sample_csvs"
saved_sample_model_path = os.path.join(directory, sample_file_name)
sample = cmdstanpy.from_csv(saved_sample_model_path)


data = {"n_drivers": df.index.nunique(),
        "n_constructors": df["TeamNumber"].nunique(),
        "n_races": df["RaceNumber"].nunique(),
        "driver_orderings": df["DriverNumber"].to_numpy(),
        "constructor_orderings": df["TeamNumber"].to_numpy()}


# Now have:
# year: year of races being looked at
# model: cmdstanpy model object, already compiled
# sample: samples from model, already computed

summary_df = sample.summary(percentiles=(5.5, 50, 94.5))

print("Summary statistics:")
print(summary_df)

index_drivers = dict(df["DriverNumber"].drop_duplicates())
index_drivers = {v: k for k, v in index_drivers.items()}
index_constructors = dict(zip(df[["TeamNumber", "TeamId"]].drop_duplicates()["TeamNumber"], df[["TeamNumber", "TeamId"]].drop_duplicates()["TeamId"]))

driver_rankings_df = pandas.DataFrame(columns = ["Mean", "SD"])
constructor_rankings_df = pandas.DataFrame(columns = ["Mean", "SD"])

for k in index_drivers:
    driver_rankings_df.loc[index_drivers[k]] = {"Mean": summary_df.loc[f't_d[{k}]', 'Mean'], "SD": summary_df.loc[f't_d[{k}]', 'StdDev']}
for k in index_constructors:
    constructor_rankings_df.loc[index_constructors[k]] = {"Mean": summary_df.loc[f't_c[{k}]', 'Mean'], "SD": summary_df.loc[f't_c[{k}]', 'StdDev']}
for k in index_drivers:
    driver_rankings_df.loc[index_drivers[k], ["TeamMean"]] = constructor_rankings_df.loc[df.loc[index_drivers[k]]["TeamId"].iloc[0]]["Mean"]
    driver_rankings_df.loc[index_drivers[k], ["TeamSD"]] = constructor_rankings_df.loc[df.loc[index_drivers[k]]["TeamId"].iloc[0]]["SD"]

driver_rankings_df["TotalMean"] = driver_rankings_df["Mean"] + driver_rankings_df["TeamMean"]
driver_rankings_df["TotalSD"] = driver_rankings_df["SD"] + driver_rankings_df["TeamSD"]

print(driver_rankings_df.sort_values(by="Mean"))
print(constructor_rankings_df.sort_values(by="Mean"))

driver_rankings_df = driver_rankings_df.sort_values(by="Mean", ascending=False)
constructor_rankings_df = constructor_rankings_df.sort_values(by="Mean", ascending=False)




matplotlib.rcParams["figure.dpi"] = 1000

figure = matplotlib.pyplot.figure(figsize=(10,6))
axis = figure.add_subplot(111)
axis.errorbar(x=range(len(driver_rankings_df["Mean"])), y=driver_rankings_df["Mean"], yerr=driver_rankings_df["SD"], fmt="o", capsize=12, color="red", ecolor="navy")
matplotlib.pyplot.xticks(range(len(driver_rankings_df["Mean"])), driver_rankings_df["Mean"].index, rotation=45, ha="center")
matplotlib.pyplot.tick_params(axis="both", labelsize=20, width=2, size=10)
matplotlib.pyplot.ylabel("Skill", fontsize=26, rotation=0, labelpad=10)
matplotlib.pyplot.xlabel("Driver", fontsize=26)
matplotlib.pyplot.tight_layout()
#matplotlib.pyplot.show()


figure = matplotlib.pyplot.figure(figsize=(9,6))
axis = figure.add_subplot(111)
axis.errorbar(x=range(len(constructor_rankings_df["Mean"])), y=constructor_rankings_df["Mean"], yerr=constructor_rankings_df["SD"], fmt="o", capsize=12, color="red", ecolor="navy")
matplotlib.pyplot.xticks(range(len(constructor_rankings_df["Mean"])), constructor_rankings_df["Mean"].index, rotation=45, ha="center")
matplotlib.pyplot.tick_params(axis="both", labelsize=20, width=2, size=10)

matplotlib.pyplot.tight_layout()
#matplotlib.pyplot.show()


figure = matplotlib.pyplot.figure(figsize=(9,6))
axis = figure.add_subplot(111)
axis.errorbar(x=range(len(driver_rankings_df["TotalMean"])), y=driver_rankings_df["TotalMean"], yerr=driver_rankings_df["TotalSD"], fmt="o", capsize=12, color="red", ecolor="navy")
matplotlib.pyplot.xticks(range(len(driver_rankings_df["TotalMean"])), driver_rankings_df["TotalMean"].index, rotation=45, ha="center")
matplotlib.pyplot.tick_params(axis="both", labelsize=20, width=2, size=10)


matplotlib.pyplot.tight_layout()

#matplotlib.pyplot.show()







figure = matplotlib.pyplot.figure(figsize=(9,6))
axis = figure.add_subplot(111)
axis.errorbar(x=range(len(driver_rankings_df["Mean"])), y=driver_rankings_df["Mean"], yerr=driver_rankings_df["SD"], fmt="o", capsize=12, color="red", ecolor="red", linewidth=0.5)
matplotlib.pyplot.xticks(range(len(driver_rankings_df["Mean"])), driver_rankings_df["Mean"].index, rotation=45, ha="center")
matplotlib.pyplot.tick_params(axis="both", labelsize=20, width=2, size=10)

axis.errorbar(x=range(len(driver_rankings_df["TotalMean"])), y=driver_rankings_df["TotalMean"], yerr=driver_rankings_df["TotalSD"], fmt="o", capsize=12, color="navy", ecolor="navy", linewidth=0.5)
matplotlib.pyplot.xticks(range(len(driver_rankings_df["TotalMean"])), driver_rankings_df["TotalMean"].index, rotation=45, ha="center")
matplotlib.pyplot.tick_params(axis="both", labelsize=20, width=2, size=10)
matplotlib.pyplot.tight_layout()

#matplotlib.pyplot.show()





figure = matplotlib.pyplot.figure(figsize=(9,6))
axis = figure.add_subplot(111)
axis.errorbar(x=range(len(driver_rankings_df["Mean"])), y=driver_rankings_df["Mean"], yerr=None, fmt="o", capsize=12, color="red", ecolor="red", linewidth=0.5, label="Driver")
matplotlib.pyplot.xticks(range(len(driver_rankings_df["Mean"])), driver_rankings_df["Mean"].index, rotation=45, ha="center")
matplotlib.pyplot.tick_params(axis="both", labelsize=20, width=2, size=10)

axis.errorbar(x=range(len(driver_rankings_df["TotalMean"])), y=driver_rankings_df["TotalMean"], yerr=None, fmt="o", capsize=12, color="navy", ecolor="navy", linewidth=0.5, label="Driver + constructor")
matplotlib.pyplot.xticks(range(len(driver_rankings_df["TotalMean"])), driver_rankings_df["TotalMean"].index, rotation=45, ha="center")
matplotlib.pyplot.tick_params(axis="both", labelsize=20, width=2, size=10)
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.legend(prop={"size":  18})
#matplotlib.pyplot.show()
matplotlib.pyplot.savefig("TotalSkill.png")


