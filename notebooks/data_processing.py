import numpy as np
import pandas as pd
import zipfile

def process_data(year):

    year = str(year)

    ############################################################
    ## import dataframe
    ############################################################

    data_file = "../data/FARS" + year + "NationalCSV.zip"

    with zipfile.ZipFile(data_file) as zip:
        with zip.open("ACCIDENT.csv") as csv:
            df = pd.read_csv(csv)

    df.columns = df.columns.str.lower()

    ############################################################
    ## COLUMN: US state
    ############################################################

    states = {
         1: "AL",  2: "AK",  4: "AZ",  5: "AR",
         6: "CA",  8: "CO",  9: "CT", 10: "DE",
        11: "DC", 12: "FL", 13: "GA", 15: "HI",
        16: "ID", 17: "IL", 18: "IN", 19: "IA",
        20: "KS", 21: "KY", 22: "LA", 23: "ME",
        24: "MD", 25: "MA", 26: "MI", 27: "MN",
        28: "MS", 29: "MO", 30: "MT", 31: "NE",
        32: "NV", 33: "NH", 34: "NJ", 35: "NM",
        36: "NY", 37: "NC", 38: "ND", 39: "OH",
        40: "OK", 41: "OR", 42: "PA", 43: "PR",
        44: "RI", 45: "SC", 46: "SD", 47: "TN",
        48: "TX", 49: "UT", 50: "VT", 51: "VA",
        52: "VI", 53: "WA", 54: "WV", 55: "WI",
        56: "WY",
    }

    df["state"] = df["state"].apply(lambda x: states[x])

    ############################################################
    ## COLUMN: case number
    ############################################################

    df.rename(columns={"st_case": "case"}, inplace=True)

    ############################################################
    ## COLUMN: date
    ############################################################

    filter_hour   = (df.hour   == 99)
    filter_minute = (df.minute == 99)

    df["second"] = 0
    df.loc[(filter_hour | filter_minute), "second"] = 30

    df.loc[filter_hour,   "hour"]   = 0
    df.loc[filter_minute, "minute"] = 0

    df["date"] = pd.to_datetime(df[["day", "month", "year", "hour", "minute", "second"]])
    df.drop(columns=["day", "month", "year", "hour", "minute", "second"], inplace=True)

    _state, _case, *cols, _date = list(df.columns)
    df = df[["state", "case", "date"] + cols]

    ############################################################
    ## COLUMN: longitude & latitude
    ############################################################

    filter_lon = (df["longitud"] > 0)

    df.loc[filter_lon, "longitud"] = -115
    df.loc[filter_lon, "latitude"] = 27

    df["lon"] = df["longitud"]
    df["lat"] = df["latitude"]

    df.drop(columns=["longitud", "latitude"], inplace=True)

    _state, _case, _date, *cols, _lon, _lat = list(df.columns)
    df = df[["state", "case", "date", "lon", "lat"] + cols]

    ############################################################
    ## COLUMN: vehicles involved
    ############################################################

    df.rename(columns={"ve_total": "vehicles"}, inplace=True)

    ############################################################
    ## COLUMN: DROP
    ############################################################

    df.drop(columns=["ve_forms"], inplace=True)
    df.drop(columns=["pvh_invl"], inplace=True)

    ############################################################
    ## COLUMN: pedestrians
    ############################################################

    df.rename(columns={"peds": "pedestrians"}, inplace=True)

    ############################################################
    ## COLUMN: DROP
    ############################################################

    df.drop(columns=["pernotmvit"], inplace=True)
    df.drop(columns=["permvit"],    inplace=True)

    ############################################################
    ## COLUMN: people & fatalities
    ############################################################

    _state, _case, _date, _lon, _lat, _vehicles, _pedestrians, _persons, *cols, _fatals, _drunk_dr = list(df.columns)
    df = df[["state", "case", "date", "lon", "lat", "vehicles", "pedestrians", "persons", "fatals", "drunk_dr"] + cols]

    ############################################################
    ## COLUMN: DROP
    ############################################################

    df.drop(columns=["county"],   inplace=True)
    df.drop(columns=["city"],     inplace=True)
    df.drop(columns=["day_week"], inplace=True)
    df.drop(columns=["nhs"],      inplace=True)
    df.drop(columns=["rur_urb"],  inplace=True)

    df.drop(columns=["func_sys"], inplace=True)
    df.drop(columns=["rd_owner"], inplace=True)
    df.drop(columns=["route"],    inplace=True)
    df.drop(columns=["tway_id"],  inplace=True)
    df.drop(columns=["tway_id2"], inplace=True)
    df.drop(columns=["milept"],   inplace=True)
    df.drop(columns=["sp_jur"],   inplace=True)
    df.drop(columns=["harm_ev"],  inplace=True)
    df.drop(columns=["man_coll"], inplace=True)
    df.drop(columns=["reljct1"],  inplace=True)
    df.drop(columns=["reljct2"],  inplace=True)
    df.drop(columns=["typ_int"],  inplace=True)
    df.drop(columns=["wrk_zone"], inplace=True)
    df.drop(columns=["rel_road"], inplace=True)
    df.drop(columns=["lgt_cond"], inplace=True)
<<<<<<< HEAD

    ############################################################
    ## COLUMN: WEATHER
    ############################################################

    cond_road = {
         0: 0,  # No Additional Atmospheric Conditions
         1: 0,  # Clear
         2: 1,  # Rain
         4: 1,  # Snow
         5: 1,  # Fog, Smog, Smoke
         6: 1,  # Severe Crosswinds
         7: 1,  # Blowing Sand, Soil, Dirt
         8: 0,  # Other
        10: 0,  # Cloudy
        11: 1,  # Blowing Snow
        12: 1,  # Freezing Rain or Drizzle
        98: 0,  # Not Reported
        99: 0,  # Unknown
    }

    df['weather0_road'] = df['weather'].map(cond_road)
    df['weather1_road'] = df['weather1'].map(cond_road)
    df['weather2_road'] = df['weather2'].map(cond_road)

    df["cond_road"] = df["weather0_road"] + df["weather1_road"] + df["weather2_road"]

    df["cond_road"] = df["cond_road"].fillna(0).astype(bool).astype(int)

    df = df.drop(columns=["weather", "weather1", "weather2", "weather0_road", "weather1_road", "weather2_road"])
    df = df.rename(columns={"cond_road": "weather"})
    
    ############################################################
    ## COLUMN: DROP
    ############################################################
    
=======
    df.drop(columns=["weather1"], inplace=True)
    df.drop(columns=["weather2"], inplace=True)

    df.drop(columns=["weather"],  inplace=True)
>>>>>>> a006bce39661b7830e41e12e1c1ea38e76cdf829
    df.drop(columns=["sch_bus"],  inplace=True)
    df.drop(columns=["rail"],     inplace=True)
    df.drop(columns=["not_hour"], inplace=True)
    df.drop(columns=["not_min"],  inplace=True)
    df.drop(columns=["arr_hour"], inplace=True)
    df.drop(columns=["arr_min"],  inplace=True)
    df.drop(columns=["hosp_hr"],  inplace=True)
    df.drop(columns=["hosp_mn"],  inplace=True)
    df.drop(columns=["cf1"],      inplace=True)
    df.drop(columns=["cf2"],      inplace=True)
    df.drop(columns=["cf3"],      inplace=True)

    ############################################################
    ## COLUMN: VIOLATIONS
    ############################################################

    with zipfile.ZipFile(data_file) as zip:
        try:
            with zip.open('VIOLATN.csv') as csv:
                df_viol = pd.read_csv(csv)
        except:
            with zip.open('Violatn.csv') as csv:
                df_viol = pd.read_csv(csv)

    df_viol.columns = df_viol.columns.str.lower()

    ## dictionary for grouping violations

    reckless = {j: "reckless" for j in range(1, 11)}
    impaired = {j: "impaired" for j in range(11, 20)}
    speeding = {j: "speeding" for j in range(21, 30)}
    other    = {j: "other"    for j in list(range(30, 100)) + [0]}

    violations = {**reckless, **impaired, **speeding, **other}

    df_viol["mviolatn"] = df_viol["mviolatn"].map(violations)

    ## prepare dataframe to merge

    df_viol = df_viol.groupby(["st_case"])["mviolatn"].agg(set)

    df_viol = pd.DataFrame(df_viol).reset_index()
    df_viol.rename(columns={"st_case": "case"}, inplace=True)

    df_viol["mviolatn"] = df_viol["mviolatn"].map(sorted)

    df_viol["impaired"] = df_viol["mviolatn"].map(lambda x: 1 if "impaired" in x else 0)
    df_viol["reckless"] = df_viol["mviolatn"].map(lambda x: 1 if "reckless" in x else 0)
    df_viol["speeding"] = df_viol["mviolatn"].map(lambda x: 1 if "speeding" in x else 0)

    ## merging violations

    df = df.merge(df_viol[["case", "reckless", "impaired", "speeding"]], on="case")

    return df


def smoothTriangle(data, degree):
    triangle=np.concatenate((np.arange(degree + 1), np.arange(degree)[::-1])) # up then down
    smoothed=[]

    for i in range(degree, len(data) - degree * 2):
        point=data[i:i + len(triangle)] * triangle
        smoothed.append(np.sum(point)/np.sum(triangle))
    # Handle boundaries
    smoothed=[smoothed[0]]*int(degree + degree/2) + smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    return smoothed
