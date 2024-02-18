# Львівська Політехніка: https://lpnu.ua

from requests import get

url = "https://lpnu.ua"
response_page = get(url + "/institutes")

print(f"Сайт університету завантажений.. Status code: {response_page.status_code}")
print("========================================")

# 3. Використовуючи бібліотеку Beautiful soap отримати список підрозділів та їх URL .
from bs4 import BeautifulSoup

page = BeautifulSoup(response_page.content, 'html.parser')
institutes_list = page.find("div", class_='view-content').find_all("div", class_='item-list')

institutes_info = []

print("Обробка інститутів........")

# Групування даних
for institute in institutes_list:
    response_department_page = get(url + institute.find("a").get('href'))
    department_page = BeautifulSoup(response_department_page.content, 'html.parser')

    # 4. Використовуючи запити отримати списки із кожної зі сторінок підрозділів.
    departments_list = department_page.find("div", class_='item-list').find("ul").find_all("li")
    departments_info = []

    for department in departments_list:
        departments_info.append(department.find("a").text)

    institutes_info.append({
        'name': institute.find("a").text.replace('інститут', ''),
        'departments_list': departments_info
    })

# Вивід даних
for institute in institutes_info:
    print("Інститут:", institute['name'])

    for department in institute['departments_list']:
        print("--- " + department)

# 5. Зберегти в файл
FILE_NAME = "Львівська політехніка.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:
    for institute in institutes_info:
        file.write("\nІнститут:" + institute['name'] + "\n")

        for department in institute['departments_list']:
            file.write("\n---:" + department + "\n")