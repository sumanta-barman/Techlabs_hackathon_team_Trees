import pandas as pd
import json

pd.set_option("display.max_rows", None, "display.max_columns", None)


def median(lst):
    return int(lst[len(lst)//2])


class Weather:
    def __init__(self, dataFrame):
        self.__dataFrame = dataFrame

    def get_max_temp(self):
        column = self.__dataFrame["Tmax"]
        values = column.values
        for i, temp in enumerate(values):
            try:
                values[i] = float(temp.replace(",", "."))
            except:
                values[i] = None
        return max([x for x in values if x is not None])

    def get_min_temp(self):
        column = self.__dataFrame["Tmin"]
        values = column.values
        for i, temp in enumerate(values):
            try:
                values[i] = float(temp.replace(",", "."))
            except:
                values[i] = 3
        return min([x for x in values if x is not None])

    def get_average_temp(self):
        column = self.__dataFrame["Tmit"]
        values = column.values
        for i, temp in enumerate(values):
            try:
                values[i] = float(temp.replace(",", "."))
            except:
                values[i] = None
        return round(median([x for x in values if x is not None]), 2)

    def get_min_ground_temp(self):
        column = self.__dataFrame["Tbod"]
        values = column.values
        for i, temp in enumerate(values):
            try:
                values[i] = float(temp.replace(",", "."))
            except:
                values[i] = None
        return min([x for x in values if x is not None])

    def get_average_sun_hours(self):
        column = self.__dataFrame["Sges"]
        values = column.values
        for i, hours in enumerate(values):
            try:
                values[i] = float(hours.replace(",", "."))
            except:
                values[i] = None
        return round(median([x for x in values if x is not None]), 2)

    def get_average_precipitation(self):
        column = self.__dataFrame["Rges"]
        values = column.values
        for i, ml in enumerate(values):
            try:
                values[i] = float(ml.replace(",", "."))
            except:
                values[i] = None
        return round(median([x for x in values if x is not None]), 2)

    def get_average_wind_speed(self):
        column = self.__dataFrame["Wmit"]
        values = column.values
        for i, kph in enumerate(values):
            try:
                values[i] = int(kph)
            except:
                values[i] = None
        return round(median([x for x in values if x is not None]), 2)

    def get_max_wind_speed(self):
        column = self.__dataFrame["WBmax"]
        values = column.values
        for i, kph in enumerate(values):
            try:
                values[i] = int(kph)
            except:
                values[i] = None
        return max([x for x in values if x is not None])


class WeatherData:
    def __init__(self):
        # Import Datasets
        df_2017 = pd.read_csv("weather_2017.csv", header=0, encoding='ascii', engine='python', delimiter=";")
        df_2018 = pd.read_csv("weather_2018.csv", header=0, encoding='ascii', engine='python', delimiter=";")
        df_2019 = pd.read_csv("weather_2019.csv", header=0, encoding='ascii', engine='python', delimiter=";")
        df_2020 = pd.read_csv("weather_2020.csv", header=0, encoding='ascii', engine='python', delimiter=";")

        # split into Winter and Summer
        winter_17 = df_2017.iloc[310:, :]
        winter_18 = df_2018.iloc[:126, :]
        self.winter_17_18 = winter_17.append(winter_18, ignore_index=True)

        self.summer_18 = df_2018.iloc[126:310, :]

        winter_18 = df_2018.iloc[310:, :]
        winter_19 = df_2019.iloc[:126, :]
        self.winter_18_19 = winter_18.append(winter_19, ignore_index=True)

        self.summer_19 = df_2019.iloc[126:310, :]

        winter_19 = df_2019.iloc[310:, :]
        winter_20 = df_2020.iloc[:126, :]
        self.winter_19_20 = winter_19.append(winter_20, ignore_index=True)

        self.summer_20 = df_2020.iloc[126:310, :]

        self.seasons = {"winter_17_18": self.winter_17_18, "summer_18": self.summer_18,
                        "winter_18_19": self.winter_18_19,
                        "summer_19": self.summer_19,
                        "winter_19_20": self.winter_19_20, "summer_20": self.summer_20}

    def get_data(self):
        years = {}
        for season in self.seasons:
            weather = Weather(self.seasons[season])
            years[season] = {
                "max_temp": weather.get_max_temp(),
                "min_temp": weather.get_min_temp(),
                "mean_temp": weather.get_average_temp(),
                "mean_sun_hours": weather.get_average_sun_hours(),
                "mean_precipitation": weather.get_average_precipitation(),
                "min_ground_temp": weather.get_min_ground_temp(),
                "mean_wind_speed": weather.get_average_wind_speed(),
                "max_wind_speed": weather.get_max_wind_speed(),
            }

        return years


if __name__ == "__main__":
    x = WeatherData()
    print(json.dumps(x.get_data(), indent=4))
