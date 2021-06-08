import csv
import re
import sys

## DATA CLEANER ###

# def clean(name, amount, unit):
printer = []
with open('ingredients.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        name = row['ingredient'].lower()
        number = row['id']
        name = name.replace('*', '')
        name = name.replace('to season', '')
        name = name.replace('to season', '')
        name = name.replace('peeled', '')
        name = name.replace('chopped', '')
        name = name.replace(' other', ' ')
        name = name.replace('pinch', '')
        name = name.replace('warm', '')
        name = name.replace('grilled', '')
        name = name.replace('cubed', '')
        name = name.replace('about', '')
        name = name.replace('roasted', '')
        name = name.replace('at least', '')
        name = name.replace('roasted', '')
        name = name.replace('mashed', '')
        name = name.replace('very', '')
        name = name.replace('ripe', '')
        name = name.replace('medium', '')
        name = name.replace('large', '')
        name = name.replace('firm', '')
        name = name.replace('weigh', '')
        name = name.replace('zest', '')
        name = name.replace(' to ', ' ')
        name = name.replace('of your choice', '')
        name = name.replace('of choice', '')
        name = name.replace('cold', '')
        name = name.replace('filter', '')
        name = name.replace('health', '')
        name = name.replace('squeeze of', '')
        name = name.replace('stalk', '')
        name = name.replace('sliced', '')
        name = name.replace('slice', '')
        name = name.replace('shredded', '')
        name = name.replace('wedge', '')
        name = name.replace('finely', '')
        name = name.replace('diced', '')
        name = name.replace('or less', '')
        name = name.replace('pieces', '')
        name = name.replace('halves', '')
        name = name.replace('for frying', '')
        name = name.replace('for cooking', '')
        name = name.replace('uncooked', '')
        name = name.replace('torn', '')
        name = name.replace('&', 'and')
        name = name.replace('squares', '')
        name = name.replace('recipe', '')
        name = name.replace('in juice', '')
        name = name.replace('grated', '')
        name = name.replace('melted', '')
        name = name.replace('-', ' ')
        name = name.replace(' med ', ' ')
        name = name.replace(' lg ', ' ')
        name = name.replace('freshly', '')
        name = name.replace('fresh', '')
        name = name.replace('fettucini', 'fettuccine')
        name = name.replace(' hot ', ' ')
        name = name.replace('mild', '')
        name = name.replace('cranks', '')
        name = name.replace('cooked', '')
        name = name.replace('bunch', '')
        name = name.replace(' approx ', ' ')
        name = name.replace('approximately', '')
        name = name.replace('approx', '')
        name = name.replace('approx.', '')
        name = name.replace('for garnish', '')
        name = name.replace('cracked', '')
        name = name.replace('shreds', 'flakes')
        name = name.replace('deveined', '')
        name = name.replace('room temperature', '')
        name = name.replace('room temp', '')
        name = name.replace('cooled', '')
        name = name.replace('chilled', '')
        name = name.replace('for serving', '')
        name = name.replace('day old', '')
        name = name.replace('preferably', '')
        name = name.replace('boiling', '')
        name = name.replace('mild', '')
        name = name.replace('removed', '')
        name = name.replace('softened', '')
        name = name.replace('minced', '')
        name = name.replace('packed', '')
        name = name.replace('drained', '')
        name = name.replace('rinsed', '')
        name = name.replace('thawed', '')
        name = name.replace('loosely', '')
        name = name.replace(',', '')
        name = name.replace('as needed', '')
        name = name.replace(' + ', 'and')
        name = name.replace('+ ', '')
        name = name.replace('taste', '')
        name = name.replace('thinly', '')
        name = name.replace('divided', '')
        name = name.replace('coarsely', '')
        name = name.replace('lb.', 'lb')
        name = name.replace('lbs.', 'lbs')
        name = name.replace('oz.', 'oz')
        name = name.replace('¾', '3/4')
        name = name.replace('½', '1/2')
        name = name.replace('⅔', '2/3')
        name = name.strip()
        
        if 'optional' in name:
            continue
        
        if name == 'generous non stick spray':
            continue

        salt = re.findall(r"\bsalt\b", name)
        if salt:
            if 'seasoning' not in name:
                continue
        if 'black pepper' in name:
            continue
        if 'cracked pepper' in name:
            continue
        
        if '$' in name:
            name = re.sub('\d+', '', name)
            name = name.replace('.', '')
            name = name.replace('$', '')

        if '/' in name:
            ind = name.index('/')
            num = re.findall('\d', name)
            if num:
                # Ex: 1 1/2 cups  water
                w = name[ind - 3]
                if re.findall('\d', w):
                    add0 = re.findall('\d', w)
                    add = int(add0[0])
                    new_amount0 = add + int(name[ind - 1]) / int(name[ind + 1])
                    new_amount = round(new_amount0, 2)
                    name = re.sub('\d \d/\d', str(new_amount), name)
                # Ex: chicken breast ( 3/4 lb)
                elif len(num) == 2:
                    new_amount0 = int(name[ind - 1]) / int(name[ind + 1])
                    new_amount = round(new_amount0, 2)
                    name = re.sub('\d/\d', str(new_amount), name)

                elif 'of a ' in name:
                    new_amount0 = int(name[ind - 1]) / int(name[ind + 1])
                    try:
                        ninth = name[ind + 9]
                        eight = name[ind + 8]
                    except IndexError:
                        print('Nothing')
                    # Ex: kale (1/2 of a 12oz bag)
                    if re.findall('\d', ninth):
                        mytuple = (eight, ninth)
                        joined = ''.join(mytuple)
                        new_amount1 = new_amount0 * int(joined)
                        new_amount = round(new_amount1, 2)
                        name = re.sub('\d/\d of a \d\d', str(new_amount), name)
                    # Ex: tomato paste (1/2 of a 6oz can)
                    else:
                        new_amount1 = new_amount0 * int(eight)
                        new_amount = round(new_amount1, 2)
                        name = re.sub('\d/\d of a \d', str(new_amount), name)
        # Delete the shit from the name after
        if 'lbs' in name:
            result = unitMaker('lbs', name)
            amount = result[0]
            unit = result[1]
        elif 'lb' in name:
            result = unitMaker('lb', name)
            amount = result[0]
            unit = result[1]
        elif 'cups' in name:
            result = unitMaker('cups', name)
            amount = result[0]
            unit = result[1]
        elif 'cup' in name:
            result = unitMaker('cup', name)
            amount = result[0]
            unit = result[1]
        elif 'oz' in name:
            indexe = name.index('oz')
            if re.findall('\d', name[indexe - 1]):
                result = unitMaker('oz', name)
                amount = result[0]
                unit = result[1]
        elif 'tbsp' in name:
            result = unitMaker('tbsp', name)
            amount = result[0]
            unit = result[1]
        elif 'tsp' in name:
            result = unitMaker('tsp', name)
            amount = result[0]
            unit = result[1]
        elif 'stick' in name:
            result = unitMaker('stick', name)
            amount = result[0]
            unit = result[1]
        elif 'handful' in name:
            unit = 'handful'
            amount = 1

        def unitMaker(nameUnit, name):
            something = name.index(nameUnit)
            if name[something - 1] != ' ':
                joiner = ' ' + nameUnit
                name = re.sub(nameUnit, joiner, name)
            new_name = name.replace('(', '')
            new_name = new_name.replace(')', '')
            splitname = new_name.split()
            with open('recipe_ingredients.csv', mode='r') as csv_file2:
                csv_reader2 = csv.DictReader(csv_file2)
                for row in csv_reader2:
                    amount = row['amount'].lower()
                    unit = row['unit'].lower()
                    if row['ingredients2_id'] == number:
                        # Clean amounts
                        amount = amount.replace('¾', '3/4')
                        amount = amount.replace('½', '1/2')
                        amount = amount.replace('⅔', '2/3')
                        if '/' in amount:
                            inde = amount.index('/')
                            num = re.findall('\d', amount)
                            many = len(num)
                            # Ex: 1/2
                            if many == 2:
                                amount = int(num[0]) / int(num[1])
                                amount = round(amount, 2)
                            elif many == 3:
                                first = amount[inde + 1]
                                try:
                                    second = amount[inde + 2]
                                except IndexError:
                                    second = 'a'
                                # Ex: 1/16
                                if re.findall('\d', second):
                                    othertuple = (first, second)
                                    joined = ''.join(othertuple)
                                    amount = int(num[0]) / int(joined)
                                    amount = round(amount, 2)
                                # Ex 1 1/4
                                else:
                                    amount = int(num[0]) + (int(num[1]) / int(num[2]))
                                    amount = round(amount, 2)
                        # If a name has NULL units
                        if not unit:
                            # Get amount from name
                            try:
                                ind = splitname.index(nameUnit)
                            except ValueError:
                                unit = nameUnit
                                return amount, unit
                            try:
                                new_amount = float(splitname[ind - 1])
                            except ValueError:
                                new_amount = 1
                                print(f'{name}')
                            # if each is in name
                            if 'each)' in splitname:
                                # multiply the lbs by the amount and save that as amount
                                amount = int(amount) * new_amount
                                amount = round(amount)
                                # save the unit
                                unit = nameUnit
                                thing = name + "," + str(amount) + "," + unit
                                printer.append(thing)
                                return amount, unit
                            else:
                                # change the amount to the name amount
                                amount = new_amount
                                # change the unit to name unit
                                unit = nameUnit
                                thing = name + "," + str(amount) + "," + unit
                                printer.append(thing)
                                return amount, unit
        
                        else:
                            thing = name + "," + str(amount) + "," + unit
                            printer.append(thing)
                            return amount, unit
                            
        
        # return name, amount, unit
        with open('names.csv', mode='a') as names_file:
            names_writer = csv.writer(names_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            names_writer.writerow([number, name])
            names_file.close()

sys.stdout = open("printer.txt", "w")
print(printer)
sys.stdout.close()
