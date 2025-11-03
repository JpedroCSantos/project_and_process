import csv

file_path = 'resources/vendedores_ativos.csv'

with open(file_path, mode='r', encoding='utf-8') as csvFile:
    reader = csv.reader(csvFile)
    next(reader, None)

    VENDEDORES_ATIVOS = {row[0] for row in reader if row}