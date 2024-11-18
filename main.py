from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
import sqlite3

conn = sqlite3.connect('recent_data.db')

c = conn.cursor()

api_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather(city):
    result = requests.get(api_url.format(city, api_key))
    if result and result.status_code == 200:
        json = result.json()
        try:
            city = json['name']
            country = json['sys']['country']
            temp_kelvin = json['main']['temp']
            temp_celsius = temp_kelvin - 273.15
            icon = json['weather'][0]['icon']
            weather = json['weather'][0]['main']
            weather_description = json['weather'][0]['description']
            humidity = json['main']['humidity']
            pressure = json['main']['pressure']
            clouds = json['clouds']['all']

            weather_results = (city, country, temp_celsius, temp_kelvin, icon, weather, weather_description, humidity,
                               pressure, clouds)
            return weather_results
        except KeyError:
            return None
    else:
        return None



def recent_weather():
    r_c1 = c.execute('SELECT * FROM recent_cities').fetchall()[-1]
    w_1 = get_weather(r_c1[0])

    r_c2 = c.execute('SELECT * FROM recent_cities').fetchall()[-2]
    w_2 = get_weather(r_c2[0])

    r_c3 = c.execute('SELECT * FROM recent_cities').fetchall()[-3]
    w_3 = get_weather(r_c3[0])

    r_c4 = c.execute('SELECT * FROM recent_cities').fetchall()[-4]
    w_4 = get_weather(r_c4[0])

    return w_1, w_2, w_3, w_4


def update_recent_city_label(city_label, city_img_label, temp_label, weather_data):
    city_label.config(text=f'{weather_data[0]}, {weather_data[1]}')

    img = PhotoImage(file=f'weather_icons/{weather_data[4]}.png')
    city_img_label.config(image=img)
    city_img_label.city_img_label = img

    temp_label.config(text=f"{round(weather_data[2])}°C")


def search():
    city = city_search.get()
    weather = get_weather(city)

    if weather:
        place_label["text"] = f'{weather[0]}, {weather[1]}'
        data_city = f'{weather[0]}, {weather[1]}'

        img = PhotoImage(file='weather_icons/{}.png'.format(weather[4]))
        data_icon = weather[4]

        weather_image['image'] = img
        weather_image.weather_image = img
        weather_temp['text'] = f'{round(weather[2]):.0f}°C'
        data_temp = round(weather[2])

        weather_label['text'] = weather[6].capitalize()
        more_info['text'] = f'Humidity: {weather[7]}%\n' \
                            f'Pressure: {weather[8]} hPa\n' \
                            f'Clouds: {weather[9]}%'

        c.execute("INSERT INTO recent_cities VALUES (?, ?, ?)", (data_city, data_icon, data_temp))

        conn.commit()

        w_1, w_2, w_3, w_4 = recent_weather()

        # Update labels for recent cities

        update_recent_city_label(recent_city_1, recent_city_1_img, recent_weather_temp_1, w_1)
        update_recent_city_label(recent_city_2, recent_city_2_img, recent_weather_temp_2, w_2)
        update_recent_city_label(recent_city_3, recent_city_3_img, recent_weather_temp_3, w_3)
        update_recent_city_label(recent_city_4, recent_city_4_img, recent_weather_temp_4, w_4)

    else:
        messagebox.showerror("Error", "Cannot find city".format(city))


app = Tk()
app.title("Spark")
app.config(padx=20, pady=20)
app.geometry('520x650')
app['bg'] = "#A9957B"


img_sp = PhotoImage(file=f'logo_spark.png')
spark_img = Label(app, image=img_sp, bg="#A9957B")
spark_img.config(height=80, width=80)
spark_img.spark_img = img_sp
spark_img.grid(row=0, column=0)

w_lab = StringVar()
spark_label = Label(app, textvariable=w_lab, font=("Arial", 40))
spark_label.config(padx=20, pady=20, bg="#A9957B")
w_lab.set("Spark")
spark_label.grid(row=0, column=1, columnspan=2)

city_search = StringVar(app, "New York")
city_entry = Entry(app, textvariable=city_search, width=30, justify=CENTER, border=8)
city_entry.grid(row=1, column=1)

search_button = Button(app, text="Search", width=12, command=search, border=6)
search_button.grid(row=1, column=2)


place_label = Label(app, text='', font=("bold", 20))
place_label.grid(row=2, column=1, columnspan=2)
place_label.config(padx=10, pady=10, bg="#A9957B")

weather_image = Label(app, image='', bg="#A9957B")
weather_image.grid(row=3, column=0, columnspan=2)

weather_temp = Label(app, text="", font=("bold", 40), bg="#A9957B")
weather_temp.grid(row=3, column=2, columnspan=2)

weather_label = Label(app, text='', bg="#A9957B")
weather_label.grid(row=4, column=0, columnspan=2)

more_info = Label(app, text='', bg="#A9957B")
more_info.grid(row=4, column=2, columnspan=2)

# RECENT CITIES

recent_cities = Label(app, text="Recent cities that you searched for:", font=("bold", 16))
recent_cities.config(padx=10, pady=20, bg="#A9957B")
recent_cities.grid(row=5, column=0, columnspan=4)

# From database take recent city and from API take current weather in this city

wea_1, wea_2, wea_3, wea_4 = recent_weather()

recent_city_1 = Label(app, text=f'{wea_1[0]}, {wea_1[1]}', font=("bold", 10), bg="#A9957B")
recent_city_1.grid(row=6, column=0)
img1 = PhotoImage(file=f'weather_icons/{wea_1[4]}.png')

recent_city_1_img = Label(app, image=img1, bg="#A9957B")
recent_city_1_img.recent_city_1_img = img1
recent_city_1_img.grid(row=7, column=0)

recent_weather_temp_1 = Label(app, text=f"{round(wea_1[2])}°C", font=("bold", 14), bg="#A9957B")
recent_weather_temp_1.grid(row=8, column=0)

recent_city_2 = Label(app, text=f'{wea_2[0]}, {wea_2[1]}', font=("bold", 10), bg="#A9957B")
recent_city_2.grid(row=6, column=1)

img2 = PhotoImage(file=f'weather_icons/{wea_2[4]}.png')
recent_city_2_img = Label(app, image=img2, bg="#A9957B")
recent_city_2_img.recent_city_2_img = img2
recent_city_2_img.grid(row=7, column=1)
recent_weather_temp_2 = Label(app, text=f"{round(wea_2[2])}°C", font=("bold", 14), bg="#A9957B")
recent_weather_temp_2.grid(row=8, column=1)

recent_city_3 = Label(app, text=f'{wea_3[0]}, {wea_3[1]}', font=("bold", 10), bg="#A9957B")
recent_city_3.grid(row=6, column=2)
img3 = PhotoImage(file=f'weather_icons/{wea_3[4]}.png')
recent_city_3_img = Label(app, image=img3, bg="#A9957B")
recent_city_3_img.recent_city_3_img = img3
recent_city_3_img.grid(row=7, column=2)
recent_weather_temp_3 = Label(app, text=f"{round(wea_3[2])}°C", font=("bold", 14), bg="#A9957B")
recent_weather_temp_3.grid(row=8, column=2)

recent_city_4 = Label(app, text=f'{wea_4[0]}, {wea_4[1]}', font=("bold", 10), bg="#A9957B")
recent_city_4.grid(row=6, column=3)
img4 = PhotoImage(file=f'weather_icons/{wea_4[4]}.png')
recent_city_4_img = Label(app, image=img4, bg="#A9957B")
recent_city_4_img.recent_city_4_img = img4
recent_city_4_img.grid(row=7, column=3)
recent_weather_temp_4 = Label(app, text=f"{round(wea_4[2])}°C", font=("bold", 14), bg="#A9957B")
recent_weather_temp_4.grid(row=8, column=3)

app.mainloop()
