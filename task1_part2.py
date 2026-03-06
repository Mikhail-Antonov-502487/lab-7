import os
import requests
from dotenv import load_dotenv

load_dotenv()


class HolidayAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://holidayapi.com/v1"
    
    def get_holidays(self, country, year, month=None):
        url = f"{self.base_url}/holidays"
        params = {
            'key': self.api_key,
            'country': country,
            'year': year
        }
        if month:
            params['month'] = month
        
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

class HolidayPrinter:
    def print_holidays(self, data, country_name):
        if not data or 'holidays' not in data:
            print("Нет данных")
            return
        
        holidays = data['holidays']
        print(f"\nПраздники в {country_name}:")
        
        K = 0
        for h in holidays:
            if K < 7:
                K+=1
                name = h.get('name', 'Неизвестно')
                date = h.get('date', 'Неизвестно')
                public = "Государственный" if h.get('public') else "Обычный"
                weekday = h.get('weekday', 'Неизвестно')['date']['name']
                uuid = h.get('uuid', 'Неизвестно')


                print(f"\n{date}")
                print(f"{name}")
                print(f"{public}")
                print(f"{weekday}")
                print(f"{uuid}")

class HolidayApp:

    def __init__(self, api_key):
        self.api = HolidayAPI(api_key)
        self.printer = HolidayPrinter()
    
    def run(self):
        print("Программа поиска праздников")
        country = input("Код страны (RU/US/GB): ").upper()
        year = input("Год (2025): ")
        
        data = self.api.get_holidays(country, year)
        self.printer.print_holidays(data, country)

if __name__ == "__main__":
    api_key = os.getenv('HOLIDAY_API_KEY')
    
    if not api_key:
        print("ОШИБКА: Не найден API ключ в переменных окружения!")
        print("Пожалуйста, создайте файл .env и добавьте туда:")
        print("HOLIDAY_API_KEY=ваш_ключ_сюда")
        print("\nИли установите переменную окружения HOLIDAY_API_KEY")
        exit(1)
    
    client = HolidayApp(api_key)
    client.run()