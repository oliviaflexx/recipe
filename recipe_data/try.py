import csv
from datacleaner import clean

# tests clean function with CSV instead of SQL database entry
with open('OGJingredients.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        with open('NEWJingredients.csv', mode='a') as names_file:
            names_writer = csv.writer(names_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            print(row['ingredient'])
            result = clean(row['ingredient'], '', '')
            if result[0] is None:
                tuplee = ('',)
            else:
                tuplee = (result[0],)
            names_writer.writerow(tuplee)
            names_file.close()
