import json


def parallel(nominals, resistors):
    r1, r2 = nominals.values()

    key_list = list(nominals.keys())
    resistors[f'{key_list[0]}{key_list[1][1:]}'] = round(r1 * r2 / (r1 + r2), 2)

    del resistors[key_list[0]]
    del resistors[key_list[1]]
    return f'{key_list[0]}{key_list[1][1:]} = {round(r1 * r2 / (r1 + r2), 2)}'


def consistent(nominals, resistors):
    r1, r2 = nominals.values()

    key_list = list(nominals.keys())
    resistors[f'{key_list[0]}{key_list[1][1:]}'] = round(r1 + r2, 2)

    del resistors[key_list[0]]
    del resistors[key_list[1]]
    return f'{key_list[0]}{key_list[1][1:]} = {round(r1 + r2, 2)}'


def to_triangle(nominals, resistors):
    result = []
    r1, r2, r3 = nominals.values()

    result.append(round(r1 + r2 + (r1 * r2) / r3, 2))
    result.append(round(r2 + r3 + (r2 * r3) / r1, 2))
    result.append(round(r1 + r3 + (r1 * r3) / r2, 2))

    key_list = list(nominals.keys())
    name_list = [chr(x) for x in range(97, 97 + 26)]
    i = 0
    while i < len(name_list):
        if f'r{name_list[i]}' in resistors:
            name_list.pop(i)
            continue
        i += 1

    a = name_list[0]
    b = name_list[1]
    c = name_list[2]

    resistors[f'r{a}'] = result[0]
    resistors[f'r{b}'] = result[1]
    resistors[f'r{c}'] = result[2]

    del resistors[key_list[0]]
    del resistors[key_list[1]]
    del resistors[key_list[2]]

    return f'r{a} = {result[0]}, r{b} = {result[1]}, r{c} = {result[2]}'


def to_star(nominals, resistors):
    result = []
    r12, r23, r13 = nominals.values()

    result.append(round(r12 * r13 / (r12 + r13 + r23), 2))
    result.append(round(r12 * r23 / (r12 + r13 + r23), 2))
    result.append(round(r23 * r13 / (r12 + r13 + r23), 2))

    key_list = list(nominals.keys())
    name_list = [chr(x) for x in range(97, 97 + 26)]
    i = 0
    while i < len(name_list):
        if f'r{name_list[i]}' in resistors:
            name_list.pop(i)
            continue
        i += 1

    a = name_list[0]
    b = name_list[1]
    c = name_list[2]

    resistors[f'r{a}'] = result[0]
    resistors[f'r{b}'] = result[1]
    resistors[f'r{c}'] = result[2]

    del resistors[key_list[0]]
    del resistors[key_list[1]]
    del resistors[key_list[2]]

    return f'r{a} = {result[0]}, r{b} = {result[1]}, r{c} = {result[2]}'


def run(resistors):
    if resistors:
        print(resistors)
    print('waiting for input, separate command by dash, nominals by comma')
    request = input()

    if request == 'save':
        with open('saves.json', 'w') as s:
            json.dump(resistors, s)
        with open('logs.txt', 'a') as f:
            f.write('saved data\n')

    request = request.split('-')

    if request[0] == 'to tr':

        with open('logs.txt', 'a') as f:
            f.write('triangle command implemented\n')
        rsstrs_for_tr = request[1]
        rsstrs_for_tr = rsstrs_for_tr.split(',')
        if len(rsstrs_for_tr) > 3:
            print(f'\ndetected more than 3 elements, will ignore exta {len(rsstrs_for_tr) - 3}\n')
        shit_for_math = {}
        for el in rsstrs_for_tr:
            shit_for_math[el] = resistors[el]

        print(to_triangle(shit_for_math, resistors))

    elif request[0] == 'to star':

        with open('logs.txt', 'a') as f:
            f.write('star command implemented\n')
        for_star = request[1]
        for_star = for_star.split(',')
        if len(for_star) > 3:
            print(f'\ndetected more than 3 elements, will ignore exta {len(for_star) - 3}\n')
        shit_for_math = {}
        for el in for_star:
            shit_for_math[el] = resistors[el]
        print(to_star(shit_for_math, resistors))

    elif request[0] == 'par':

        with open('logs.txt', 'a') as f:
            f.write('parallel command implemented\n')
        rsstrs_for_par = request[1]
        rsstrs_for_par = rsstrs_for_par.split(',')
        if len(rsstrs_for_par) > 2:
            print(f'\ndetected more than 2 elements, will ignore exta {len(rsstrs_for_par) - 2}\n')
        shit_for_math = {}
        for el in rsstrs_for_par:
            shit_for_math[el] = resistors[el]
        print(parallel(shit_for_math, resistors))

    elif request[0] == 'const':

        with open('logs.txt', 'a') as f:
            f.write('consistent command implemented\n')
        rsstrs_for_const = request[1]
        rsstrs_for_const = rsstrs_for_const.split(',')
        if len(rsstrs_for_const) > 2:
            print(f'\ndetected more than 2 elements, will ignore exta {len(rsstrs_for_const) - 2}\n')
        shit_for_math = {}
        for el in rsstrs_for_const:
            shit_for_math[el] = resistors[el]
        print(consistent(shit_for_math, resistors))

    elif request[0] == 'help':
        with open('logs.txt', 'a') as f:
            f.write('asked for help\n')
        print(
            'first, provide program with nominals, like this: r1=x,r2=y,r3...\n '
            'then input transform type:\n '
            'to tr: star - triangle\n '
            'to star: triangle - star\n '
            'par: 2 parallel resistors to 1\n '
            'const: 2 consistent resistors to 1\n '
        )

    run(resistors)


def launch():
    print('give me nominals, separated by comma without spaces\n')
    specs = input()
    resistors = {}

    if specs == 'help':
        print(
            'first, provide program with nominals, like this: r1=x,r2=y,r3...\n'
            'then input transform type:\n'
            'to tr: star - triangle\n'
            'to star: triangle - star\n'
            'par: 2 parallel resistors to 1\n'
            'const: 2 consistent resistors to 1\n'
            'use default: set default values\n'
            'save: save resistors\n'
            'load: load last save\n'
        )
        with open('logs.txt', 'a') as f:
            f.write('asked for help\n')
        launch()

    elif specs == 'use default':
        with open('logs.txt', 'a') as f:
            f.write('using default nominals\n')
            resistors = {'r1': 909, 'r2': 1250, 'r3': 200, 'r4': 162, 'r5': 140, 'r6': 162, 'r7': 1470}
            f.write('received nominals\n')
        run(resistors)

    elif specs == 'load':
        with open('saves.json', 'r') as load:
            resistors = json.load(load)
        with open('logs.txt', 'a') as f:
            f.write('loaded last save\n')
        run(resistors)

    specs = specs.split(',')

    for el in specs:
        el = el.split('=')
        try:
            resistors[el[0]] = float(el[1])
        except:
            print('Invalid input, restarted')
            launch()

    with open('logs.txt', 'a') as f:
        f.write('received nominals\n')
    run(resistors)


with open('logs.txt', 'a') as f:
    f.write('started new session\n')
    launch()

# TODO: подумать как сделать связи (узел n связан с узлом k номиналом R: n-R-k например)
# TODO: сделать тесты (в процессе)
# TODO: подумать как тут пропихнуть ООП можно сделать класс резисторов, объектами будут резисторы
#  или класс цепи, с элементами и связями
# TODO: сделать больше фиксов ошибок
# TODO: переписать функции, убрать повторяющийся код