import numpy
import pandas
import cmdstanpy
import matplotlib.pyplot
import matplotlib

matplotlib.rcParams["figure.dpi"] = 1000

year = 2023

# loading data
data_file = f"project/f1_data_year{year}.pkl"
data = pandas.read_pickle(data_file)


drivers = ["MAG", "HUL"]


n = 22

fig, axes = matplotlib.pyplot.subplots(1, 2, sharey=True, figsize=(10,4))


matplotlib.pyplot.subplot(1, 2, 1)
driver = drivers[0]
driver_data = data.loc[driver]
grid = numpy.array(driver_data["GridPosition"])
grid[grid == 0] = 20
pos = numpy.array(driver_data["Position"])
summ = numpy.cumsum(pos)
count = numpy.arange(1, len(pos) + 1)
ave = summ / count
x = list(range(n))
axes[0].plot(x, ave, color="navy", label="Average finish")
axes[0].plot(x, pos, color="red", label="Actual finish")
axes[0].plot(x, grid, alpha=0.25, color="red", label="Starting")
axes[0].set_title(driver + " race positions", fontsize=14)
axes[0].set_xlabel("Race number", fontsize=14)


matplotlib.pyplot.subplot(1, 2, 2)
driver = drivers[1]
driver_data = data.loc[driver]
grid = numpy.array(driver_data["GridPosition"])
grid[grid == 0] = 20
pos = numpy.array(driver_data["Position"])
summ = numpy.cumsum(pos)
count = numpy.arange(1, len(pos) + 1)
ave = summ / count
x = list(range(n))
axes[1].plot(x, ave, color="navy", label="Average finish")
axes[1].plot(x, pos, color="red", label="Actual finish")
axes[1].plot(x, grid, alpha=0.25, color="red", label="Starting")
axes[1].set_title(driver + " race positions", fontsize=14)
axes[1].set_yticks([1, 5, 10, 15, 20])
axes[1].set_xlabel("Race number", fontsize=14)
axes[0].set_ylabel("Position", fontsize=14)
axes[0].tick_params(axis="both", labelsize=10)
axes[1].tick_params(axis="both", labelsize=10)

axes[0].legend(loc="upper left")


matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig("exploratory.png")





















