import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

FILE_PATH = 'feeds.csv'


def read_data_pd(file_path):
    df = pd.read_csv(file_path,
                     index_col=0,
                     parse_dates=True,
                     usecols=[0, 2, 3, 4, 5, 6, 7])
    df.rename(columns={'field1': 'temperature_1',
                       'field3': 'temperature_2',
                       'field5': 'temperature_3',
                       'field2': 'humidity_1',
                       'field4': 'humidity_2',
                       'field6': 'humidity_3'},
              inplace=True)
    return df


def draw_vs(sensors):
    for key in sensors.keys():
        temp, hum = sensors[key]
        fig, ax = plt.subplots(figsize=(16, 9))
        plt.title("Temperatures vs humidity for " + key + ", data correlation: " + str(hum.corr(temp)))
        ax.plot(data.index, temp, color='r', label="Temperature")
        ax.set_xlabel("date")
        ax.set_ylabel("Temperature")
        ax2 = ax.twinx()
        ax2.plot(data.index, hum, color='b', label="Humidity")
        ax2.set_ylabel("Humidity")
        fig.tight_layout()
        fig.legend(loc="upper left")
        plt.savefig("./img/Temperature vs humidity " + key)


def draw(temps, hums, mean=True):
    if mean is True:
        hums['mean'] = hums.mean(axis=1)
        temps['mean'] = temps.mean(axis=1)
    plt.figure(figsize=(16, 9))
    plt.title("Temperatures & humidity across 2 weeks")
    plt.subplot(211)
    data['temperature_1'].plot()
    data["temperature_2"].plot()
    data["temperature_3"].plot()
    temps["mean"].plot()
    plt.ylabel("Temperatures [C°]")
    plt.legend(loc='best')

    plt.subplot(212)
    data['humidity_1'].plot()
    data["humidity_2"].plot()
    data["humidity_3"].plot()
    hums["mean"].plot()
    plt.ylabel("Humidity [%]")
    plt.legend(loc='best')
    plt.savefig("./img/Temperature and humidity with means") if mean \
        else plt.savefig("./img/Temperature and humidity")

    plt.figure(figsize=(16, 9))


def draw_daily(data):
    daily_data = data.resample('D').mean()[1:]
    fig, ax = plt.subplots(figsize=(16, 9))
    plt.title("Daily temperature and humidity")
    ax.plot(daily_data["temperature_1"], color='orange', label="temperature_1")
    ax.plot(daily_data["temperature_2"], color='goldenrod', label="temperature_2")
    ax.plot(daily_data["temperature_3"], color='darkorange', label="temperature_3")
    ax.set_xlabel("date")
    ax.set_ylabel("Temperature")
    ax.grid()
    ax2 = ax.twinx()
    ax2.plot(daily_data["humidity_1"], color='royalblue', label="humidity_1")
    ax2.plot(daily_data["humidity_2"], color='mediumblue', label="humidity_2")
    ax2.plot(daily_data["humidity_3"], color='blue', label="humidity_3")
    ax2.set_ylabel("Humidity")
    fig.legend(loc="upper left")
    fig.tight_layout()
    plt.savefig("./img/Daily temperature vs humidity ")


def draw_corr(data):
    plt.figure(figsize=(12, 10))
    plt.title("Correlation between all inputs")
    sns.heatmap(data=data.corr(), cmap="rocket", annot=True)


def draw_pairs(data, combined=True, pairs=True):
    daily_data = data.resample('D').mean()[1:]

    if combined or (not combined and not pairs):
        sns.pairplot(daily_data, corner=True)
        # plt.title("Temperature from humidity for")
        plt.savefig('./img/Graph of temperature from humidity')
    if pairs or (not combined and not pairs):
        snippet = daily_data[['temperature_1', 'humidity_1']]
        sns.pairplot(snippet, kind='scatter').fig.set_size_inches(10, 10)
        # plt.title("Temperature from humidity for sensor 1")
        plt.savefig('./img/Graph of temperature from humidity for sensor 1')

        snippet = daily_data[['temperature_2', 'humidity_2']]
        sns.pairplot(snippet, kind='scatter').fig.set_size_inches(10, 10)
        # plt.title("Temperature from humidity for sensor 2")
        plt.savefig('./img/Graph of temperature from humidity for sensor 2')

        snippet = daily_data[['temperature_3', 'humidity_3']]
        sns.pairplot(snippet, kind='scatter').fig.set_size_inches(10, 10)
        # plt.title("Temperature from humidity for sensor 3")
        plt.savefig('./img/Graph of temperature from humidity for sensor 3')


if __name__ == "__main__":
    data = read_data_pd(FILE_PATH)
    temps = data[['temperature_1', 'temperature_2', "temperature_3"]].copy(deep=True)
    hums = data[['humidity_1', 'humidity_2', 'humidity_3']].copy(deep=True)

    sensors = {
        "sensor 1": [data['temperature_1'], data['humidity_1']],
        "sensor 2": [data['temperature_2'], data['humidity_2']],
        "sensor 3": [data['temperature_3'], data['humidity_3']],
    }

    draw_daily(data)
    draw_pairs(data)
    draw_corr(data)
    draw_vs(sensors)
    draw(temps, hums)
    draw(temps, hums, mean=True)
