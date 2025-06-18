from key import WEATHER_KEY, IP_KEY
import requests
from io import BytesIO
from PIL import Image
import customtkinter
import datetime

def get_ip():
    return requests.get("https://api.ipify.org").text

def get_location(ip):
    lat_lon_request = requests.get(f"https://api.ip2location.io/?key={IP_KEY}&ip={ip}")
    lat_lon = lat_lon_request.json()
    return lat_lon["latitude"], lat_lon["longitude"]

def get_weather(lat, lon):
    weather_request = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_KEY}&lang=ru&units=metric"
    )
    return weather_request.json()

def update_weather():
    try:
        ip = get_ip()
        lat, lon = get_location(ip)
        weather = get_weather(lat, lon)

        description = weather["weather"][0]["description"].capitalize()
        name = weather["name"]
        temp = round(weather["main"]["temp"])
        feels_like = round(weather["main"]["feels_like"])
        icon_code = weather["weather"][0]["icon"]

        time = datetime.datetime.now().strftime("%H:%M:%S")

        label_city.configure(text=f"Город: {name}")
        weather_desc.configure(text=f"Погода: {description}")
        temp_label.configure(text=f"Температура: {temp}°C")
        feels_label.configure(text=f"Ощущается как: {feels_like}°C")
        time_label.configure(text=f"Время обновления: {time}")

        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_data = requests.get(icon_url).content
        img = Image.open(BytesIO(icon_data))
        icon = customtkinter.CTkImage(light_image=img, dark_image=img, size=(100, 100))

        icon_label.configure(image=icon)
        icon_label.image = icon

    except Exception as e:
        label_city.configure(text="Ошибка при получении данных")
        print("Ошибка:", e)

app = customtkinter.CTk()
app.title("Weather app")
app.geometry("600x450")

label_city = customtkinter.CTkLabel(app, text="Город: ", font=("Helvetica", 14))
label_city.pack(pady=10)

weather_desc = customtkinter.CTkLabel(app, text="Погода: ", font=("Helvetica", 14))
weather_desc.pack()

icon_label = customtkinter.CTkLabel(app, text="")
icon_label.pack(pady=5)

temp_label = customtkinter.CTkLabel(app, text="Температура: ", font=("Helvetica", 14))
temp_label.pack(pady=10)

feels_label = customtkinter.CTkLabel(app, text="Ощущается как: ", font=("Helvetica", 14))
feels_label.pack(pady=10)

time_label = customtkinter.CTkLabel(app, text=f"Время обновления: ")
time_label.pack(pady=15)

update_button = customtkinter.CTkButton(app, text="Обновить погоду", command=update_weather)
update_button.pack(pady=10)

update_weather()
app.mainloop()
