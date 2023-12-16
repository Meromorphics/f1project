import pandas
import fastf1
import os

# gets and stores a pandas dataframe object, where each row is indexed by driver abbreviation, 
# and for each indexed row contains the race name that the driver took place in for that row,
# finishing position, starting position, and team name
# additionally, gives each race, driver, and constructor a unique integer identifier; for use in STAN

# Example entry:
# Abbreviation          Position     GridPosition     TeamId     Race     RaceNumber     TeamNumber     DriverNumber
# MAG                   10           4                haas  Miami Grand Prix   5         9              13

n = 22 # number of races
year = 2023 # year to get results from


# Preparing dataframe by loading the first race
# dataframe to be stored is called master
session = fastf1.get_session(year, 1, "Race")
session.load()
session.results.set_index("Abbreviation", inplace=True)
master = session.results[["Position", "GridPosition", "TeamId"]]
master["Race"] = session.event["EventName"]
master["RaceNumber"] = 1

# loading in the rest of the races
for i in range(2, n + 1):
    session = fastf1.get_session(year, i, "Race")
    session.load()
    session.results.set_index("Abbreviation", inplace=True)
    df = session.results[["Position", "GridPosition", "TeamId"]]
    df["Race"] = session.event["EventName"]
    df["RaceNumber"] = i
    master = pandas.concat([master,df], ignore_index=False)

# in 2023, there was a nan value in the dataset that belongs to Stroll
if year == 2023:
    master.rename(index={"nan": "STR"}, inplace=True)

# assigning driver and constructor unique integer identifiers
driver_dictionary = dict()
for i, abbreviation in enumerate(master.index.unique(), start=1):
    driver_dictionary[abbreviation] = i
constructor_dictionary = dict()
for i, team in enumerate(master["TeamId"].unique(), start=1):
    constructor_dictionary[team] = i
master["TeamNumber"] = master["TeamId"].map(constructor_dictionary)
master["DriverNumber"] = master.index.map(driver_dictionary)

# UNCOMMENT IF driver_constructor_circuit_model.stan IS DESIRED TO BE USED
# CIRCUIT TYPE DATA MUST BE IMPLEMENTED MANUALLY.
# COMMENTED OUT SINCE THIS MODEL PERFORMS THE WORST AND CAN EASILY LEAD TO COMPILATION
# ERRORS SINCE IT RELIES ON MANUALLY IMPLEMENTED DATA.
# ONE LINE IN THE FOLLOWING CODE BLOCK MUST ALSO BE UNCOMMENTED.
# -------------------------------------------------------------------------

# dictionary that tells if a circuit is a street or race circuit
# THIS DICTIONARY MUST BE IMPLEMENTED MANUALLY
circuit_types = {"Bahrain Grand Prix": "Race",
                 "Saudi Arabian Grand Prix": "Street",
                 "Australian Grand Prix": "Street",
                 "Azerbaijan Grand Prix": "Street",
                 "Miami Grand Prix": "Street",
                 "Monaco Grand Prix": "Street",
                 "Spanish Grand Prix": "Race",
                 "Canadian Grand Prix": "Street",
                 "Austrian Grand Prix": "Race",
                 "British Grand Prix": "Race",
                 "Hungarian Grand Prix": "Race",
                 "Belgian Grand Prix": "Race",
                 "Dutch Grand Prix": "Race",
                 "Italian Grand Prix": "Race",
                 "Singapore Grand Prix": "Street",
                 "Japanese Grand Prix": "Race",
                 "Qatar Grand Prix": "Race",
                 "United States Grand Prix": "Race",
                 "Mexico City Grand Prix": "Race",
                 "Las Vegas Grand Prix": "Street",
                 "Abu Dhabi Grand Prix": "Race",
                "German Grand Prix": "Race",
                "Brazilian Grand Prix": "Race",
                "São Paulo Grand Prix": "Race",
                "Styrian Grand Prix": "Race",
                "San Marino Grand Prix": "Race",
                "Emilia Romagna Grand Prix": "Race",
                "Mexican Grand Prix": "Race",
                "Argentine Grand Prix": "Race",
                "Sakhir Grand Prix": "Race",
                "South African Grand Prix": "Race",
                "Malaysian Grand Prix": "Race",
                "French Grand Prix": "Race",
                "Chinese Grand Prix": "Race",
                "European Grand Prix": "Race",
                "Portuguese Grand Prix": "Race",
                "Turkish Grand Prix": "Race"}
circuit_type_index = {"Race": 0, "Street": 1}

master["CircuitType"] = master["Race"].map(circuit_types)
master["CircuitTypeIndex"] = master["CircuitType"].map(circuit_type_index)

# -------------------------------------------------------------------------
# END OPTIONAL UNCOMMENTING


# forcing entries that should be integers to be integers; for example some were stored as 7.0
master["Position"] = master["Position"].astype(int)
master["GridPosition"] = master["GridPosition"].astype(int)
master["TeamNumber"] = master["TeamNumber"].astype(int)
master["DriverNumber"] = master["DriverNumber"].astype(int)
# UNCOMMENT FOLLOWING LINE IF CIRCUIT TYPE MODEL IS DESIRED
master["CircuitTypeIndex"] = master["CircuitTypeIndex"].astype(int)

# saving dataframe
directory = os.path.dirname(os.path.realpath(__file__))
file_name = f"f1_data_year{year}.pkl"
saved_path = os.path.join(directory, file_name)
master.to_pickle(saved_path)
print(f"Saved dataframe in the file f1_data_year{year}.pkl")
