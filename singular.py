import csv
from datacleaner import clean

# tests clean function with CSV instead of SQL database entry
with open('OGingredient.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        with open('table3.csv', mode='a') as names_file:
            names_writer = csv.writer(names_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            result = clean(row['ingredient'], row['amount'], row['unit'])
            tuplee = (row['recipe'], result[0], result[1], result[2])
            names_writer.writerow(tuplee)
            names_file.close()
