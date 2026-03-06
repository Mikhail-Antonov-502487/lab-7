import os
import requests
from dotenv import load_dotenv
load_dotenv()


class WeatherAPI:
     
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather_data(self, city_name):
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        
        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None


class WeatherPrinter:
    
    def print_weather(self, city_name, data):
        if not data:
            print("Нет данных для отображения")
            return
        
        try:
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            
            print(f"ПОГОДА В ГОРОДЕ {city_name.upper()}")
            print(f"Описание: {weather_desc.capitalize()}")
            print(f"Температура: {temp:.1f}°C")
            print(f"Ощущается как: {feels_like:.1f}°C")
            print(f"Влажность: {humidity}%")
            print(f"Давление: {pressure} гПа")
            
        except KeyError as e:
            print(f"Ошибка в данных: отсутствует поле {e}")


class WeatherClient:
    
    def __init__(self, api_key):
        self.api = WeatherAPI(api_key)
        self.printer = WeatherPrinter()
    
    def get_weather(self, city_name):
        print(f"Запрашиваю погоду для {city_name}...")
        data = self.api.get_weather_data(city_name)
        self.printer.print_weather(city_name, data)
        return data


if __name__ == "__main__":
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if not api_key:
        print("ОШИБКА: Не найден API ключ в переменных окружения!")
        print("Пожалуйста, создайте файл .env и добавьте туда:")
        print("OPENWEATHER_API_KEY=ваш_ключ_сюда")
        exit(1)
    
    client = WeatherClient(api_key)
    city = "Warsaw"
    client.get_weather(city)
