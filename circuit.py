import eqres


class Element:

    def __init__(self, first_node, second_node, resistance):
        self.nodes = [first_node, second_node]
        self.resistance = resistance


def input_manager():
    print('give nominals')
    user_input = input()

    if user_input == 'use default':
        resistors = {
            'R1': Element('a', 'd', 909),
            'R2': Element('a', 'e', 1250),
            'R3': Element('b', 'd', 200),
            'R4': Element('a', 'b', 162),
            'R5': Element('f', 'd', 140),
            'R6': Element('b', 'c', 162),
            'R7': Element('e', 'f', 1470),
            'V': Element('a', 'c', 0),
            'A': Element('d', 'e', float('inf'))
        }
    else:
        user_input = user_input.split(',')
        user_input = [el.split('-') for el in user_input]
        resistors = {}
        i = 1
        while user_input:
            elem = user_input[0]
            if elem[2] == '0':
                resistors['V'] = Element(elem[0], elem[1], 0)
            elif elem[2] == 'inf':
                resistors['A'] = Element(elem[0], elem[1], float('inf'))
            else:
                resistors[f'R{i}'] = Element(elem[0], elem[1], int(elem[2]))
                i += 1
            user_input.pop(0)
    return resistors


def run():
    resistors = input_manager()

    for el in resistors.values():
        print(el.nodes, el.resistance)


run()

# TODO сделать прогу чтоб сама преобразовывала цепь в эквивалентный резистор
# TODO добавить тесты
# TODO добавить try на случай юзверя
