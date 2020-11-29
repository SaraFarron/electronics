import json


def triangle_calcs(r1, r2, r3):
    return [round(r1 + r2 + (r1 * r2) / r3, 2), round(r2 + r3 + (r2 * r3) / r1, 2), round(r1 + r3 + (r1 * r3) / r2, 2)]


def star_calcs(r1, r2, r3):
    return [round(r1 * r3 / (r1 + r3 + r2), 2), round(r1 * r2 / (r1 + r3 + r2), 2), round(r2 * r3 / (r1 + r3 + r2), 2)]


def three_res(nominals, resistors, mode):
    r1, r2, r3 = nominals.values()
    if mode:
        result = triangle_calcs(r1, r2, r3)
    else:
        result = star_calcs(r1, r2, r3)

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


def two_calcs(nominals, resistors, mode):
    r1, r2 = nominals.values()

    if mode:
        result = const_calcs(r1, r2)
    else:
        result = par_calcs(r1, r2)

    key_list = list(nominals.keys())
    resistors[f'{key_list[0]}{key_list[1][1:]}'] = result

    del resistors[key_list[0]]
    del resistors[key_list[1]]
    return f'{key_list[0]}{key_list[1][1:]} = {result}'


def const_calcs(r1, r2):
    return round(r1 + r2, 2)


def par_calcs(r1, r2):
    return round(r1 * r2 / (r1 + r2), 2)


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
    try:
        for_transform = request[1]
        for_transform = for_transform.split(',')
    except:
        if request[0] == 'help':
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

    if len(for_transform) > 3:
        print(f'\ndetected more than 3 elements, will ignore exta {len(for_transform) - 3}\n')

    shit_for_math = {}
    for el in for_transform:
        shit_for_math[el] = resistors[el]

    if request[0] == 'to tr':

        with open('logs.txt', 'a') as f:
            f.write('triangle command implemented\n')

        print(three_res(shit_for_math, resistors, True))

    elif request[0] == 'to star':

        with open('logs.txt', 'a') as f:
            f.write('star command implemented\n')

        print(three_res(shit_for_math, resistors, False))

    elif request[0] == 'par':

        with open('logs.txt', 'a') as f:
            f.write('parallel command implemented\n')

        print(two_calcs(shit_for_math, resistors, False))

    elif request[0] == 'const':

        with open('logs.txt', 'a') as f:
            f.write('consistent command implemented\n')

        print(two_calcs(shit_for_math, resistors, True))

    else:
        raise_error()

    run(resistors)


def raise_error():
    print('Invalid input, restarted')
    with open('logs.txt', 'a') as f:
        f.write('Error took place, new session started\n')
    launch()


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

    if len(specs) < 2:
        raise_error()

    for el in specs:
        el = el.split('=')
        try:
            resistors[el[0]] = float(el[1])
        except:
            raise_error()

    with open('logs.txt', 'a') as f:
        f.write('received nominals\n')

    run(resistors)


if __name__ == '__main__':
    launch()

# TODO: сделать тесты (в процессе)
