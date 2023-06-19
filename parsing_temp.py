from requests import get
from bs4 import BeautifulSoup

def make_http_request(m: str, city: str):
    """Формирование запроса и получения html-кода старницы"""
    url = f"https://yandex.ru/pogoda/{city}/month/{m}"
    request_get = get(url)
    return request_get.text if request_get.status_code == 200 else ""

def find_temps(html):
    """Поиск и взятие данных о теператур на странице"""

    soup = BeautifulSoup(html, "lxml")
    divs = soup.select("div.climate-calendar-day:not([class*=climate-calendar-day_colorless_yes])") # берет только дни, входящие в месяц
    day_temps, night_temps = [], []
    for div in divs:
        day_t = find_day_temp(div)
        night_t = find_night_temp(div)

        day_temps.append(check_number_temp(day_t))
        night_temps.append(check_number_temp(night_t))
        
    return day_temps, night_temps

def find_day_temp(div):
    """Находит дневную температуру"""
    day_temp_block = div.find("div", class_ = "temp climate-calendar-day__temp-day") # берет блок с дневной температурой
    day_temp = day_temp_block.find("span", class_= "temp__value temp__value_with-unit").text # извлекаем температуру
    return day_temp

def find_night_temp(div):
    """Находит ночную температуру"""
    night_temp_block = div.find("div", class_ = "temp climate-calendar-day__temp-night") # берет блок с дневной температурой
    night_temp = night_temp_block.find("span", class_= "temp__value temp__value_with-unit").text # извлекаем температуру
    return night_temp

def check_number_temp(number: str):
    """Преобразует температуру строкового типа в целое число с учетом знака"""
    if "−" in number:
        return (-1) * int(number.replace("−", ""))
    return int(number)

def load_data_temps(month: str, name_city: str):
    """Загрузка температур с сайта"""
    data = make_http_request(month, name_city) # получам html-код страницы
    day_temps, night_temps =  find_temps(data) # достаем данные о теператур со страницы
    return day_temps, night_temps
