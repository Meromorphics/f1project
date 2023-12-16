import numpy
import pandas
import cmdstanpy
import matplotlib.pyplot
import matplotlib

matplotlib.rcParams["figure.dpi"] = 1000

year = 2023

# loading data
sample_csv_folder = f"project/year{year}_driver_constructor_model_sample_csvs"
data_file = f"project/f1_data_year{year}.pkl"
sample = cmdstanpy.from_csv(sample_csv_folder)
data = pandas.read_pickle(data_file)


# dictionary with driver index : team index of driver as entries
driver_team_pairings = data.groupby("DriverNumber")["TeamNumber"].apply(set).to_dict()
for key, value in driver_team_pairings.items():
    driver_team_pairings[key] = value.pop()
driver_team_pairings

# dictionary with driver abbreviation : driver index as entries
driver_index_pairings = data.groupby(data.index)["DriverNumber"].apply(set).to_dict()
for key, value in driver_index_pairings.items():
    driver_index_pairings[key] = value.pop()
driver_index_pairings


# storing sample results as a dataframe: df
df = sample.draws_pd()

# getting driver theta's from df: df_d
# column i : theta of driver with index i
driver_n = data["DriverNumber"].max()
df_d = df[["t_d[1]", "t_d[2]"]].copy()
for i in range(3, driver_n + 1):
    df_d[f"t_d[{i}]"] = df[f"t_d[{i}]"].copy()

# getting constructor theta's from df:
# column i : theta of team with index i
constructor_n = data["TeamNumber"].max()
df_c = df[["t_c[1]", "t_c[2]"]].copy()
for i in range(3, constructor_n + 1):
    df_c[f"t_c[{i}]"] = df[f"t_c[{i}]"].copy()
    
# relabeling df_d, df_c columns to natural numbers
df_d.columns = range(1, driver_n + 1)
df_c.columns = range(1, constructor_n + 1)

# column i : theta of team driver with index i is on
df_driver_team = pandas.DataFrame({key: df_c[value] for key, value in driver_team_pairings.items()})

# column i : total theta of driver with index i
df_theta = df_d + df_driver_team

# equation 2 of Glickman and Hennessy
# performances are drawn from gumbel distribution with location theta (and scale 1)
simulated_performances = df_theta.apply(numpy.random.gumbel)

points = 300 # how many points from sample to use in posterior predictive inference; restriction: race_n * points < sample amount
race_n = data["RaceNumber"].max()
# setting a drivers performance to NaN if they did not participate in a race
for i in range(1, race_n + 1):
    driver_indices = data.loc[data["RaceNumber"] == i]["DriverNumber"].to_numpy()
    simulated_performances.loc[slice((i-1)*points, i*points), df_d.columns.difference(driver_indices)] = numpy.nan
# simulated result = rank ordering of performances for each race (position 1 if highest performance draw, ..., position 20 if lowest performance draw)
simulated_races = simulated_performances.rank(axis=1, ascending=False).astype("Int64")
simulated_races = simulated_races.iloc[:race_n * points + 1] # only the first race_n * points rows are simulated




# select a key from driver_index_pairings
driver = "HAM"

# normalized histogram of simulated race results 
simulated_races[driver_index_pairings[driver]].plot(kind="hist", 
                                                    density=True, 
                                                    bins=range(1,22), 
                                                    edgecolor="black", 
                                                    align="left", 
                                                    alpha=0.9, 
                                                    label="Simulated", 
                                                    color="navy")

# normalized histogram of actual race results
data.loc[driver]["Position"].plot(kind="hist", 
                                  density=True, 
                                  bins=range(1,22), 
                                  edgecolor="black", 
                                  align="left", 
                                  alpha=0.7, 
                                  label="Real", 
                                  color="red")

matplotlib.pyplot.xticks(range(1, 21), range(1, 21))
matplotlib.pyplot.title(f"Actual compared to simulated race results for {driver}", fontsize=16)
matplotlib.pyplot.ylabel("Frequency", fontsize=16)
matplotlib.pyplot.xlabel("Finishing position", fontsize=16)
matplotlib.pyplot.tick_params(axis="both", labelsize=12, width=2, size=8)
matplotlib.pyplot.legend()
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig(f"{driver}.png")
#matplotlib.pyplot.show()






# Two drivers to show side by side
drivers = ["LAW", "DEV"]

figure, axes = matplotlib.pyplot.subplots(1, 2, figsize=(12, 6), sharey=True)

for i, driver in enumerate(drivers):
    simulated_races[driver_index_pairings[driver]].plot(kind="hist", 
                                                        density=True, 
                                                        bins=range(1, 22), 
                                                        edgecolor="black", 
                                                        align="left", 
                                                        alpha=0.9, 
                                                        label="Simulated", 
                                                        color="navy",
                                                        ax=axes[i])

    # Normalized histogram of actual race results
    data.loc[driver]["Position"].plot(kind="hist", 
                                      density=True, 
                                      bins=range(1, 22), 
                                      edgecolor="black", 
                                      align="left", 
                                      alpha=0.7, 
                                      label="Real", 
                                      color="red",
                                      ax=axes[i])

    axes[i].set_xticks(range(1, 21))
    axes[i].tick_params(axis="y", which="major", labelsize=16)
    axes[i].tick_params(axis="x", which="major", labelsize=12)
    axes[i].set_title(f"Actual vs Simulated for {driver}", fontsize=22)
    axes[i].set_xlabel("Finishing position", fontsize=22)


axes[0].set_ylabel("Frequency", fontsize=22)
matplotlib.pyplot.legend()
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig(f"post_{drivers[0]}_{drivers[1]}.png")




