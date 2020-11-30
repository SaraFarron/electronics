import json


class Element:

    def __init__(self, resistance):
        self.resistance = resistance


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
    name_list = [chr(x).upper() for x in range(97, 97 + 26)]
    i = 0
    while i < len(name_list):
        if f'r{name_list[i]}' in resistors:
            name_list.pop(i)
            continue
        i += 1

    a = name_list[0]
    b = name_list[1]
    c = name_list[2]

    resistors[f'R{a}'] = Element(result[0])
    resistors[f'R{b}'] = Element(result[1])
    resistors[f'R{c}'] = Element(result[2])

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
    resistors[f'{key_list[0]}{key_list[1][1:]}'] = Element(result)

    del resistors[key_list[0]]
    del resistors[key_list[1]]
    return f'{key_list[0]}{key_list[1][1:]} = {result}'


def const_calcs(r1, r2):
    return round(r1 + r2, 2)


def par_calcs(r1, r2):
    return round(r1 * r2 / (r1 + r2), 2)


def input_manager():
    print('give me nominals, separated by comma without spaces\n')
    user_input = input()

    if user_input == 'use default':
        with open('logs.txt', 'a') as f:
            f.write('using default nominals\n')
            f.write('received nominals\n')
        resistors = {
            'R1': Element(909),
            'R2': Element(1250),
            'R3': Element(200),
            'R4': Element(162),
            'R5': Element(140),
            'R6': Element(162),
            'R7': Element(1470),
            'V': Element(0),
            'A': Element(float('inf'))
        }

    elif user_input == 'help':
        provide_help()
        launch()
    elif user_input == 'load':
        with open('saves.json', 'r') as load:
            tmp = json.load(load)

        resistors = {}
        for v, k in tmp.items():
            resistors[f'k'] = Element(v)

        with open('logs.txt', 'a') as f:
            f.write('loaded last save\n')
        # run(resistors)
    else:
        user_input = user_input.split(',')
        resistors = {}
        i = 1
        while user_input:
            elem = user_input[0]
            if elem == '0':
                resistors['V'] = Element(0)
            elif elem == 'inf':
                resistors['A'] = Element(float('inf'))
            else:
                resistors[f'R{i}'] = Element(int(elem))
                i += 1
            user_input.pop(0)

    with open('logs.txt', 'a') as f:
        f.write('received nominals\n')
    return resistors


def raise_error():
    print('Invalid input, restarted')
    with open('logs.txt', 'a') as f:
        f.write('Error took place, new session started\n')
    launch()


def provide_help():
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


def run(resistors):
    if resistors:
        for k in resistors.keys():
            print(f'{k}: ', resistors[f'{k}'].resistance)
    print('waiting for input, separate command by dash, elements by comma')
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
        elems = resistors.keys()
        for v in for_transform:
            if v not in elems:
                raise_error()
    except:
        if request[0] == 'help':
            provide_help()
            run(resistors)

    if len(for_transform) > 3:
        print(f'\ndetected more than 3 elements, will ignore exta {len(for_transform) - 3}\n')

    shit_for_math = {}
    for el in for_transform:
        shit_for_math[el] = resistors[el].resistance

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


def launch():
    resistors = input_manager()
    run(resistors)


if __name__ == '__main__':
    launch()
