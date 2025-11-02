import csv

file_path = 'resources/categorias_validas.csv'

with open(file_path, mode='r', encoding='utf-8') as csvFile:
    reader = csv.reader(csvFile)
    next(reader, None)

    CATEGORIAS_VALIDAS = {row[0] for row in reader if row}