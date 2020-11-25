# same as eqres.py but with OOP
class Element:
    count = 1

    def __init__(self, resistance):
        self.resistance = resistance
        self.name = f'r{self.count}'
        self.count += 1
