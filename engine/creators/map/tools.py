from ...systems.commands import get_command

class Tools():
    def get_position(self, axis, max_value):
        while True:
            try:
                value = get_command(f"Enter {axis} for pointer: ")
                if value == None:
                    continue
                value = int(value)
                if value <= 0:
                    print("Invalid number! Type only numbers larger than 0.")
                elif value > max_value:
                    print(f"Invalid number! Max number you can type is: {max_value}")
                    value = 0
                else:
                    value -= 1
                    return value
            except ValueError:
                print("Wrong number. Type only whole numbers.")
            except Exception:
                print("Something went wrong")

class Pointer(Tools):
    def __init__(self, name, y, x):
        self.name = name
        self.y = y
        self.x = x
    
    def place(self, map_structure, structure):
        map_structure[self.y][self.x] = structure

class Liner(Tools):
    def __init__(self, name, f_y, f_x, s_y, s_x):
        self.name = name
        self.f_y = f_y
        self.f_x = f_x
        self.s_y = s_y
        self.s_x = s_x

    def place(self, map_structure, structure):
        x1, y1 = self.f_x, self.f_y
        x2, y2 = self.s_x, self.s_y

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        err = dx - dy

        while True:
            map_structure[y1][x1] = structure

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x1 += sx

            if e2 < dx:
                err += dx
                y1 += sy

class Square(Tools):
    def __init__(self, name, f_y, f_x, s_y, s_x):
        self.name = name
        self.f_y = f_y
        self.f_x = f_x
        self.s_y = s_y
        self.s_x = s_x

    def place(self, map_structure, structure):
        y1, x1 = self.f_y, self.f_x
        y2, x2 = self.s_y, self.s_x

        dy = abs(y1 - y2)
        dx = abs(x1 - x2)

        sy = 1 if y1 < y2 else -1
        sx = 1 if x1 < x2 else -1

        for i in range(0, dy):
            map_structure[y1][x1] = structure
            map_structure[y2][x2] = structure
            y1 += sy
            y2 -= sy

        for i in range(0, dx):
            map_structure[y1][x1] = structure
            map_structure[y2][x2] = structure
            x1 += sx
            x2 -= sx

pointer = Pointer("POINTER", 0, 0)
liner = Liner("LINER", 0, 0, 0, 0)
square = Square("SQUARE", 0, 0, 0, 0)

if __name__ == '__main__':
    pointer.get_position(False, 5)