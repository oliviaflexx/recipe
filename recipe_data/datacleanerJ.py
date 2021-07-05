# coding=utf-8
import re
import sys
import inflect

## DATA CLEANER function for database ###
p = inflect.engine()

def clean(name, amount, unit):

    name = name.lower()
    if 'cracked pepper' in name:
        amount = None
        name = None
        unit = None
        return name, amount, unit

    if 'optional' in name:
        amount = None
        name = None
        unit = None
        return name, amount, unit
    
    if 'non stick spray' in name:
        amount = None
        name = None
        unit = None
        return name, amount, unit

    salt = re.findall(r"\bsalt\b", name)
    if salt:
        if 'seasoning' not in name and 'black' not in name and 'breadcrumbs' not in name and 'zucchini' not in name and 'seasoning' not in name:
            amount = None
            name = None
            unit = None
            return name, amount, unit

    if 'black pepper' in name:
        amount = None
        name = None
        unit = None
        return name, amount, unit

    if 'ground pepper' in name:
        amount = None
        name = None
        unit = None
        return name, amount, unit

    water = re.findall(r"\bwater\b", name)
    if water:
        if '+' not in name and 'or' not in name and 'coconut' not in name and 'soaked' not in name and 'sparkling' not in name:
            amount = None
            name = None
            unit = None
            return name, amount, unit
####

    # Clean the amounts
    if amount:
        amount = amount.replace('¼', '1/4')
        amount = amount.replace('⅛', '1/8')
        amount = amount.replace('¾', '3/4')
        amount = amount.replace('½', '1/2')
        amount = amount.replace('⅔', '2/3')

        amount = amount.strip()

        if '-' in amount:
            indexy = amount.index('-')
            try:
                if amount[indexy + 2] != '/':
                    if not re.findall('-$', amount):
                        amount = re.sub('-.*', '', amount)
                else:
                    amount = amount.replace('-',' ')
            except IndexError:
                print('IndexError caught')

        if 'to' in amount:
            amount = re.sub('to.*', '', amount)
        if 'or' in amount:
            amount = re.sub('or.*', '', amount)
            
        amount = amount.strip()

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

        splitamount = amount.split()
        if len(splitamount) == 2:
            amount = float(splitamount[0]) * float(splitamount[1])

        # Not sure of this
        amount = re.sub("[^0-9\.]", "", str(amount))
        amount = re.sub('\.$', '', str(amount))
        amount = amount.strip()

    if unit:
        unit = unit.lower()
        if '-' in unit:
            unit = re.sub('-', '', unit)

        num = re.findall('\d', unit)
        many = len(num)
        if re.findall('[\d]*[.][\d]+', unit):
            dotnum = re.findall('[\d]*[.][\d]+', unit)
            amount = float(amount) * float(dotnum[0])
        if many == 2:
            tuple1 = (num[0], num[1])
            joined = ''.join(tuple1)
            amount = float(amount) * float(joined)
        elif many == 1:
            amount = float(amount) * float(num[0])
        unit = unit.replace('.', '')
        
        if 'lbs' in unit:
            unit = 'lb'
        if 'cups' in unit:
            unit = 'cup'
        if 'cloves' in unit:
            unit = 'clove'

        if 'oz' in unit:
            unit = 'oz'
        
        if 'handful' in unit and not amount:
            amount = '1'
        unit = unit.strip()

    name = name.lower()
    name = name.replace('*', '')
    name = name.replace('cubed', '')
    name = name.replace('cubes', '')

    name = name.replace('from', '')
    name = name.replace('roughly', '')
    name = name.replace('peeled', '')
    name = name.replace('chopped', '')
    name = name.replace(' other', ' ')
    name = name.replace('pinch', '')
    name = name.replace('warmed', '')
    name = name.replace('warm', '')
    name = name.replace('grilled', '')
    name = name.replace('well', '')
    name = name.replace('or one', '')
    name = name.replace('bullion', 'bouillon')
    name = re.sub('\Wreal','', name)
    name = name.replace('raman', 'ramen')
    name = name.replace('about', '')
    name = name.replace('at least', '')
    name = name.replace('rolled', '')
    name = name.replace('sized', '')
    name = name.replace('size', '')
    name = name.replace('total', '')
    name = name.replace('thick and rich', '')
    name = name.replace('fillet', 'filet')
    name = name.replace('spicy or regular', '')

    ### Save roasted for fire roasted tomatoes ###
    if 'fire' not in name:
        name = name.replace('roasted', '')
    if '5 spice' in name:
        name = name.replace('5', 'five')
    name = name.replace('mashed', '')
    name = name.replace('very', '')
    name = name.replace('ripe', '')
    name = name.replace('large', '')
    if 'tofu' not in name:
        name = name.replace('firm', '')
    name = name.replace('weigh', '')
    name = name.replace('zested', '')
    name = name.replace('zest', '')
    name = name.replace(' to ', ' ')
    name = name.replace('of your choice', '')
    name = name.replace('of choice', '')
    name = name.replace('cold', '')
    name = name.replace('envelope', '')
    name = name.replace('health', '')
    name = name.replace('squeeze of', '')
    name = name.replace('stalk', '')
    name = name.replace('sliced', '')
    name = name.replace('slices', '')
    name = name.replace('slice', '')
    name = name.replace('soft taco', '')
    name = name.replace('drummette', 'drumette')
    name = name.replace('olek', 'oelek')
    name = name.replace('portabello', 'portobello')
    name = re.sub(u"[èéêë]", 'e', name)
    name = name.replace('deveigned', '')
    if 'coconut' not in name:
        name = name.replace('shredded', '')
    name = name.replace('wedge', '')
    name = name.replace('finely', '')
    name = name.replace('diced', '')
    name = name.replace('sturdy', '')
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
    name = name.replace('xlg ', ' ')
    name = name.replace('lg ', ' ')
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
    name = name.replace('removed', '')
    name = name.replace('softened', '')
    name = name.replace('minced', '')
    name = name.replace('packed', '')
    name = name.replace('drained', '')
    name = name.replace('rinsed', '')
    name = name.replace('thawed', '')
    name = name.replace('loosely', '')
    if ' or ' not in name:
        name = name.replace(',', '')
    name = name.replace('as needed', '')
    name = name.replace(' + ', 'and')
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
    name = name.replace('lg ', ' ')
    name = name.replace('small', '')
    name = name.replace('crowns', '')
    name = name.replace('crown', '')
    name = name.replace('floret', '')
    name = name.replace('smooth', '')
    name = name.replace('for coating the muffin tin', '')
    name = name.replace(' ea ', '')
    name = name.replace('splash of', '')
    name = re.sub('^med ', 'medium', name)
    
    name = name.replace('med.', 'medium')

    name = name.replace('medium', '')
    name = name.replace('plus some for dusting', '')
    name = name.replace('any flavor', '')
    name = name.replace('whit ', 'white ')
    name = name.replace('granule', '')

    name = name.replace('any color', '')
    name = name.replace('any shape', '')
    name = name.replace('style', '')
    name = name.replace('for dipping', '')

    if 'chicken' not in name and 'milk' not in name and 'pita' not in name:
        name = name.replace('whole', '')
    name = name.replace('prepared', '')
    name = name.replace('with juices', '')
    name = name.replace('with juice', '')
    name = name.replace('slightly', '')
    name = name.replace('lightly', '')
    name = name.replace('beaten', '')

    if 'butter' in name:
        name = name.replace('sticks', '')
        name = name.replace('stick', '')
    name = name.replace('whites only', '')
    name = name.replace('in half', '')
    name = name.replace('monterrey', 'monterey')
    name = name.replace('portobella', 'portobello')
    name = name.replace('worchestershire', 'worcestershire')
    name = name.replace('breadcrumb', 'bread crumb')
    name = name.replace('diameter your preference', '')
    name = name.replace('any variety', '')
    name = name.replace('stemmed and cut', '')
    name = name.replace('crumbled', '')
    name = name.replace('separated', '')

    if 'egg' in name:
        name = name.replace('soft', '')
        name = name.replace('boiled', '')
        name = name.replace('fried', '')
    name = name.replace('for the skillet', '')
    name = name.replace('for pan frying', '')
    name = name.replace('bag ', '')
    name = name.replace('bags ', '')
    name = name.replace('from a salad bar', '')
    name = name.replace('pkg ', '')
    name = name.replace('batch ', '')
    name = name.replace('yolk ', '')
    name = name.replace('pcs', '')
    name = name.replace('prepared', '')
    name = name.replace('for pizza', '')
    name = name.replace('ball ', '')
    name = re.sub('soft bread won\'t cut it!', '', name)
    name = name.replace('seasoning packets discarded', '')

    if 'celery' in name:
        name = name.replace('ribs', '')
        unit = 'rib'
    if 'ears' in name and not unit:
        name = name.replace('ears', '')
        unit = 'ears'
    if 'dashes' in name:
        name = name.replace('dashes', '')
        unit = 'dashes'

    if 'garlic' in name:
        if not unit:
            name = name.replace('cloves', '')
            name = name.replace('clove', '')
            if 'bulb' in name:
                unit = 'bulb'
            else:
                unit = 'clove'

    if 'loaf' in name:
        name = name.replace('loaf', '')
        unit = 'loaf'

    if 'juiced' in name:
        if unit is None:
           name = name.replace('juiced', '')
        else:
            name = name.replace('juiced', 'juice')
    if 'curly leaf kale' in name:
        name = 'kale'
    name = name.strip()
    

    
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

            #spinach (two  handfuls or 1/4 of an 8oz bag)
            elif 'or 1/4 of an 8oz bag' in name:
                name = name.replace('spinach (two  handfuls or 1/4 of an 8oz bag)', 'spinach 2 oz')

            elif len(num) == 3 and 'of' in name:
                new_amount0 = int(name[ind - 1]) / int(name[ind + 1])
                try:
                    seven = name[ind + 7]
                    six = name[ind + 6]
                except IndexError:
                    print('Nothing')
                # red peppers (1/2 of 12oz jar)
                if re.findall('\d', seven):
                    mytuple = (six, seven)
                    joined = ''.join(mytuple)
                    new_amount1 = new_amount0 * int(joined)
                    new_amount = round(new_amount1, 2)
                    name = re.sub('\d/\d of \d\d', str(new_amount), name)
                # 'baby spinach (1/2 of 8oz bag)'
                else:
                    new_amount1 = new_amount0 * int(six)
                    new_amount = round(new_amount1, 2)
                    name = re.sub('\d/\d of \d', str(new_amount), name)

    def unitMaker(nameUnit, name, amount, unit):
        something = name.index(nameUnit)
        # Change this to check if its lb in the name or not
        if name[something - 1] != ' ':
            joiner = ' ' + nameUnit
            name = re.sub(nameUnit, joiner, name)
        new_name = name.replace('(', '')
        new_name = new_name.replace(')', '')
        splitname = new_name.split()
        nothing = ''
        name = re.sub(nameUnit, nothing, name)

        digit = re.findall('\d', name)
        startplus = re.findall('\^\+', name)

        if unit == 'lbs' or unit == 'lb':
            counter = 1
        elif '+' in name or 'plus' in name:
            counter = 1
            name = name.replace('+ ', '')
            name = name.replace('plus', '')
        elif len(digit) == 0:
            counter = 1
        else:
            counter = 0
        if not unit or counter == 0:
            # Get amount from name
            try:
                indexx = splitname.index(nameUnit)
            except ValueError:
                unit = nameUnit
            try:
                new_amount = float(splitname[indexx - 1])
            except ValueError or UnboundLocalError:
                new_amount = 1
            # if each is in name
            if 'each)' in splitname:
                # multiply the lbs by the amount and save that as amount
                amount = int(amount) * new_amount
                amount = round(amount)
                # save the unit
                unit = nameUnit
            else:
                # change the amount to the name amount
                amount = new_amount
                # change the unit to name unit
                unit = nameUnit
            
        return amount, unit, name

    # Delete the shit from the name after
    if 'lbs' in name:
        result = unitMaker('lbs', name, amount, unit)
        amount = result[0]
        unit = result[1]
        name = result[2]
    elif 'lb' in name:
        if not re.findall('\Slb', name):
            result = unitMaker('lb', name, amount, unit)
            amount = result[0]
            unit = result[1]
            name = result[2]
    elif 'cups' in name:
        result = unitMaker('cups', name, amount, unit)
        amount = result[0]
        unit = result[1]
        name = result[2]
    elif 'cup' in name:
        result = unitMaker('cup', name, amount, unit)
        amount = result[0]
        unit = result[1]
        name = result[2]
    elif 'oz' in name:
        indexe = name.index('oz')
        if re.findall('\d', name[indexe - 1]) or re.findall('\d', name[indexe - 2]):
            result = unitMaker('oz', name, amount, unit)
            amount = result[0]
            unit = result[1]
            name = result[2]
    elif 'tbsp' in name:
        result = unitMaker('tbsp', name, amount, unit)
        amount = result[0]
        unit = result[1]
        name = result[2]
    elif 'tsp' in name:
        result = unitMaker('tsp', name, amount, unit)
        amount = result[0]
        unit = result[1]
        name = result[2]
    elif 'handful' in name:
        unit = 'handful'
        name = name.replace('handful', '')
        amount = 1
    
    name  = re.sub('\(.*?\)', '', name)
    name = re.sub(' into.*', '', name)
    name = re.sub('^to ', '', name)
    name = re.sub('"', '', name)
    name = re.sub('\.', '', name)

    if 'inch' not in name and '"' not in name and '%' not in name and '″' not in name:
        name = re.sub('\d', '', name)

    name = name.strip()
    name = re.sub('^oz ', '', name)
    name = re.sub('^and ', '', name)
    name = re.sub('^s ', '', name)
    name = re.sub('^of ', '', name)
    name = re.sub('^or ', '', name)
    name = re.sub('^few ', '', name)
    name = re.sub('^or ', '', name)
    name = re.sub('^links ', '', name)
    name = re.sub('^head ', '', name)
    name = re.sub('^pre ', '', name)
    name = name.replace('w/', 'with')
    name = name.replace('/', ' or ')
    name = re.sub('thin$', '', name)
    
    name = re.sub('and$', '', name)
    name = re.sub('crushed$', '', name)

    if re.findall('^a ', name):
        name = re.sub('^a ', '', name)
        amount = '1'

    name = ' '.join(name.split())
    name = name.strip()

    if 'not' in name:
        split_string = name.split('not', 1)
        name = split_string[0]

    
    isit = p.singular_noun(name)

    if isit is not False and 'hummus' not in name and 'molasses' not in name and 'asparagus' not in name and 'couscous' not in name:
        name = p.singular_noun(name)

    # Manual changes
    name = name.replace('8 inch four tortilla', '8 inch flour tortilla')
    name = name.replace('berry cranberry sauce', 'cranberry sauce')
    name = name.replace('chops thick cut pork chop', 'thick cut pork chop')
    name = name.replace('kimchi kimchi juice', 'kimchi')
    name = name.replace('french bread long', 'french bread')
    name = name.replace('lemon juice lemon', 'lemon juice')
    if re.findall('^one', name):
        name = name.replace('one', '')
        amount = '1'
    if name == 'french':
        name = 'french bread'
    name = name.replace('frozen and shrimp', 'frozen shrimp')
    name = name.replace('lg egg', 'egg')
    name = name.replace('one lemon', 'lemon')
    name = name.replace('pizza dough for pizza', 'pizza dough')
    name = name.replace('pork butt roast boston butt', 'pork butt roast')
    name = name.replace('roma tomatoes or one tomato', 'roma tomato')
    name = name.replace('dry old fashioned oat', 'old fashioned oat')

    if name == 'thick and rich pizza sauce':
        name = 'pizza sauce'

    if 'sriracha' in name:
        name = 'siracha'

    if name == 'egg white' or name == 'egg yolk' or name == 'extra egg':
        name = 'egg'

    if re.findall('and juice$', name):
        name = name.replace('and juice', 'juice')

    name = name.replace('crushed or tomato', 'crushed tomato')
    name = name.replace('lemon cut', 'lemon')
    name = name.replace('lemon or lime, juice', 'lemon or lime juice')
    name = name.replace('tortilla chip strip', 'tortilla strip')
    name = name.replace('blueberries, frozen', 'frozen blueberries')
    name = name.replace('pineapple canned', 'pineapple can')
    name = name.replace('juice a lime', 'lime juice')
    name = name.replace('lemon, or juice', 'lemon juice')
    name = name.replace('garlic, crushed', 'garlic')
    name = name.replace('pepperandsauce chipotle pepper in adobo', 'peppers chipotle pepper in adobo')
    name = re.sub('\Wor$', '', name)
    name = re.sub(',$', '', name)
    name = name.strip()

    if unit:
        unit = unit.replace('bags', 'bag')
        unit = unit.replace('boxes', 'box')
        unit = unit.replace('cups', 'cup')
        unit = unit.replace('dashes', 'dash')
        unit = unit.replace('handfull', 'handful')
        unit = unit.replace('inches', 'inch')
        unit = unit.replace('tbso', 'tablespoon')
        unit = unit.replace('tbps', 'tablespoon')
        unit = unit.replace('tbsp', 'tablespoon')
        unit = unit.replace('tbs', 'tablespoon')
        unit = unit.replace('pinches', 'pinch')
        unit = unit.replace('pints', 'pint')
        unit = unit.replace('quarts', 'quart')
        unit = unit.replace('thick slices', 'slice')
        unit = unit.replace('slices', 'slice')
        unit = unit.replace('small clove', 'clove')
        if unit == 'lb':
            unit = unit.replace('lb', 'pound')
        unit = unit.replace('lbs', 'pound')
        unit = unit.replace('tsp (or less)', 'teaspoon')
        unit = unit.replace('tsp', 'teaspoon')
        unit = unit.replace('pkg', 'package')
        unit = unit.replace('oz', 'ounce')
        unit = unit.replace('ounces', 'ounce')
        unit = unit.replace('ears', 'cob')
        unit = unit.replace('cobs', 'cob')
        unit = unit.replace('links', 'link')
        unit = unit.replace('grams', 'gram')
        unit = unit.replace('sprigs', 'sprig')

        if unit == 'small' or unit == 'medium' or unit == 'large' or unit == 'yellow' or unit == 'whole' or unit == 'ball' or unit == 'pieces':
            unit = ''

    return name, amount, unit