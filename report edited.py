import csv
from random import choice, uniform, randint
!pip install faker 
from faker import Faker
from collections import defaultdict 

DEP_MARKETING = 'Маркетинг'
DEP_SALES = 'Продажи'
DEP_DEVEL = 'Разработка'
DEP_ANALYTICS = 'Аналитика'
DEP_ACCOUNTING = 'Бухгалтерия'
DEP_ALL = (
    DEP_MARKETING,
    DEP_SALES,
    DEP_DEVEL,
    DEP_ANALYTICS,
    DEP_ACCOUNTING,
)

OCCUPATION_BY_DEP = {
    DEP_MARKETING: ('Маркетинг-менеджер', ),
    DEP_SALES: ('Sales manager', 'Key account manager'),
    DEP_DEVEL: (
        'iOS-инженер',
        'Android-инженер',
        'Backend-инженер',
        'Frontend-инженер',
        'Продакт-менеджер',
    ),
    DEP_ACCOUNTING: ('Бухгалтер', ),
    DEP_ANALYTICS: ('ML-инженер', 'Data Science инженер', ),
}

AREA_BY_DEP = {
    DEP_MARKETING: ('Direct', 'Performance', ),
    DEP_SALES: ('B2C', 'B2B', 'Госы', ),
    DEP_DEVEL: ('Платформа', 'Основной продукт', 'Внутренний портал', ),
    DEP_ACCOUNTING: ('Компенсации и льготы', 'Зарплата', ),
    DEP_ANALYTICS: ('DWH', 'Product', ),
}

REPORT_HEADER_FIELDS = (
    'ФИО полностью',
    'Департамент',
    'Отдел',
    'Должность',
    'Оценка',
    'Оклад',
)

SALARY_MIN = 55000
SALARY_MAX = 125000

PERF_SCORE_MIN = 3.5
PERF_SCORE_MAX = 5.0


faker_gen = Faker('ru_RU')
with open('./My_new_file.csv', 'w') as f:
    out_file = csv.writer(f, delimiter=';')
    out_file.writerow(REPORT_HEADER_FIELDS)
    for _ in range(200):
        dep_name = choice(DEP_ALL)
        area_name = choice(AREA_BY_DEP[dep_name])
        occupation = choice(OCCUPATION_BY_DEP[dep_name])

        out_file.writerow((
            faker_gen.name(),
            dep_name,
            area_name,
            occupation,
            '{:3.1f}'.format(uniform(PERF_SCORE_MIN, PERF_SCORE_MAX)),
            randint(SALARY_MIN, SALARY_MAX) // 100 * 100,
        ))



def hierarchy(): 

  """Функция считывает инфо из csv файла и выводит иерархические отношение Департаментов 
  и входящие в них отделы в соотвествие с отношениями элементов внутри словаря,
  где Д. - ключ, О. - значения"""

  with open('./My_new_file.csv', newline='') as csvFile:
    csv_Reader = csv.DictReader(csvFile, delimiter = ';')
    depart_team = defaultdict(set)
    for row in csv_Reader:
      depart_team[row['Департамент']].add(row['Отдел'])
      
    print('\nСписок всех депаратментов и отделов:\n')
    for department, team in depart_team.items():
      print("{0}:{1}".format(department,team))


def report(): 
  
  """ Функция считывает инфо из csv файла и возвращает сводный отчет из данных: 
  названия департамента, средней ЗП, минимуму и максимум по вилке, численостью"""

  with open('./My_new_file.csv', newline='') as csvFile: 
    csv_Reader = csv.DictReader(csvFile, delimiter = ';')
    salary = defaultdict(list)
    for row in csv_Reader:
      salary_departments = int(row['Оклад'])
      salary[row['Департамент']].append(salary_departments)
    
    for department, wage in salary.items():
      print("\n{0} : {1} руб ".format(department, (sum(wage) // len(wage))),'- средняя ЗП', 
            min(wage),'руб','- min вилки,',
            max(wage), 'руб','- max вилки,',
            len(wage),'чел.','- численность')


def save_csv_report(): 

  """ Здесь мы записываем csv файл с итоговым сводным отчетом по департаментам"""
  
  with open('./My_new_file.csv', newline='') as csvFile: 
    csv_Reader = csv.DictReader(csvFile, delimiter = ';')
    salary = defaultdict(list)
    for row in csv_Reader:
      salary_departments = int(row['Оклад'])
      salary[row['Департамент']].append(salary_departments)
     
    for department, wage in salary.items():
      salary[department] = [sum(wage) // len(wage), min(wage), max(wage), len(wage)]

    with open('./report.csv','w') as csvFile:
      header = ['Департамент', 'Средняя ЗП', 'Min.ЗП', 'Max.ЗП','Численность']
      csv_Writer = csv.DictWriter(csvFile, fieldnames = header)
      csv_Writer.writeheader()
      for department, wage in salary.items():
        csvWriter.writerow({'Департамент' : department, 'Средняя ЗП' : sum(wage) // len(wage), 
                      'Min.ЗП' : min(wage),'Max.ЗП': max(wage),'Численность' :  len(wage)})
    
    
if __name__ == '__main__': 

  option = ''
  options = {'1':hierarchy,
             '2':report,
             '3':save_csv_report}
  while option not in options:
    print('Выберите:\n',
          '1 -- Вывести иерархию отделов\n',
          '2 -- Вывести сводный отчёт по отделам\n',
          '3 -- Сохранить сводный отчёт в виде csv-файла',
          )
    option = input()

  options[option]()
