import csv
from random import choice, uniform, randint
!pip install faker
from faker import Faker


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

  ''' Функция считывает инфо из csv файла и выводит иерархические отношение Департаментов 
  и входящие в них отделы в соотвествие с отношениями элементов внутри словаря,
  где Д. - ключ, О. - значения'''

  with open('./My_new_file.csv', newline='') as csvFile:
    csvReader = csv.DictReader(csvFile, delimiter = ';') #  считываем файл с разделелитем по строкам
    res = {} # создаем пустой словарь для записи уникальных значений департаментов и соотв.отделов
    for row in csvReader:
      if row['Департамент'] not in res: 
        res[row['Департамент']] = [] # в словаре создаем пустой список с названиями департаментов
        res[row['Департамент']].append(row['Отдел']) #добавляем отдел в депаратмент 
      else: # проверяем если отдел уже есть в департаменте в значениях словаря, если нет - добавляем
          if row['Отдел'] in [x for v in res.values() for x in v]: 
              pass
          else: 
            res[row['Департамент']].append(row['Отдел'])
    
    print('\nСписок всех депаратментов и отделов:\n')
    for key, value in res.items():
      print("{0}:{1}".format(key,value))


def report(): 
  
  ''' Функция считывает инфо из csv файла и возвращает сводный отчет из данных: 
  названия департамента, средней ЗП, минимуму и максимум по вилке, численостью'''

  with open('./My_new_file.csv', newline='') as csvFile: 
    csvReader = csv.DictReader(csvFile, delimiter = ';')
    sal = {}
    for row in csvReader:

      if row['Департамент'] not in sal: 
        sal[row['Департамент']] = [] # в словаре создаем пустой список с названиями департаментов
        salary_departments = int(row['Оклад']) #преобразуем ЗП в числа
        sal[row['Департамент']].append(salary_departments) #добавляем ЗП по  депаратментам
      else: # проверяем если ЗП уже есть в департаменте в значениях словаря, если нет - добавляем
        if row['Оклад'] in [x for v in sal.values() for x in v]: 
          pass
        else: 
          sal[row['Департамент']].append(salary_departments)
    
    for key, value in sal.items():
      print("\n{0} : {1} руб ".format(key, (sum(value) // len(value))),'- средняя ЗП,',
            min(value),'руб','- min вилки,',
            max(value), 'руб','- max вилки,',
            len(value),'чел.','- численность')
      
    # for key, value in sal.items():
    #   print("{0} : {1}".format(key, (sum(value) // len(value))),
    #         min(value),
    #         max(value),
    #         len(value))

def save_csv_report(): 

  """ Здесь мы записываем csv файл с итоговым сводным отчетом по департаментам"""
  
  with open('./My_new_file.csv', newline='') as csvFile: 
    csvReader = csv.DictReader(csvFile, delimiter = ';')
    sal = {}
    for row in csvReader:
      if row['Департамент'] not in sal: 
        sal[row['Департамент']] = [] # в словаре создаем пустой список с названиями департаментов
        salary_departments = int(row['Оклад']) #преобразуем ЗП в числа
        sal[row['Департамент']].append(salary_departments) #добавляем ЗП по  депаратментам
      else: # проверяем если ЗП уже есть в департаменте в значениях словаря, если нет - добавляем
        if row['Оклад'] in [x for v in sal.values() for x in v]: 
          pass
        else: 
          sal[row['Департамент']].append(salary_departments)
    
    for key,value in sal.items():
      sal[key] = [sum(value) // len(value), min(value), max(value), len(value)]

    with open('./report.csv','w') as csvFile:
      header = ['Департамент', 'Средняя ЗП', 'Min.ЗП', 'Max.ЗП','Численность']
      csvWriter = csv.DictWriter(csvFile, fieldnames = header)
      csvWriter.writeheader()
      for key,value in sal.items():
        csvWriter.writerow({'Департамент' : key, 'Средняя ЗП' : sum(value) // len(value), 
                      'Min.ЗП' : min(value),'Max.ЗП': max(value),'Численность' :  len(value)})
    
# with open('./report.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row['Департамент'], row['Средняя ЗП'], row['Min.ЗП'])
    
if __name__ == '__main__': 

  option = ''
  options = range(1, 4)
  while option not in options:
    print('Выберите:\n',
          '1 -- Вывести иерархию отделов\n',
          '2 -- Вывести сводный отчёт по отделам\n',
          '3 -- Сохранить сводный отчёт в виде csv-файла',
          )
    option = int(input())

  if option == 1:
    hierarchy()
  elif option == 2:
    report()
  elif option == 3:
    save_csv_report()
  else:
    print('Выберите число команды в предложенном списке')

