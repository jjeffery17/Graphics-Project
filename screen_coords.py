import time
import numpy as np
import math

def unique_list(l: list) -> list:
    out = []
    for i in l:
        if i not in out:
            out.append(i)
    return out

def vector_addition(a: list[float], b: list[float]) -> list[float]:
    if len(a) != len(b):
        raise ValueError("Length of a and b are not equal")
    out = []
    for i in range(len(a)):
        out.append(a[i] + b[i])
    return out

def vector_subtraction(a: list[float], b: list[float]) -> list[float]:
    if len(a) != len(b):
        raise ValueError("Length of a and b are not equal")
    out = []
    for i in range(len(a)):
        out.append(a[i] - b[i])
    return out

def vector_size(a: list[float]) -> float:
    total = 0
    for item in a:
        total += item*item
    return math.sqrt(total)

def vector_multiplication(a: list[float], b: float) -> list[float]:
    out = []
    for item in a:
        out.append(item*b)
    return out

def vector_division(a: list[float], b: float) -> list[float]:
    out = []
    for item in a:
        out.append(item/b)
    return out

class World:
    def __init__(self, screenx, screeny, fov=90.0):
        self.screenx = screenx
        self.screeny = screeny
        self.screenratio = screeny/screenx
        self.hfov = fov
        self.vfov = 2 * math.degrees(math.atan(math.tan(math.radians(self.hfov/2)) * self.screenratio))
        print(f"hfov: {self.hfov}   vfov: {self.vfov}   screen ratio: {self.screenratio}")
        self.screen = np.zeros([screeny, screenx, 3])
        self.world_vertices = []
        self.world_faces = []
    def update_screen(self):
        start = time.process_time()
        '''self.screen = np.zeros([self.screeny, self.screenx, 3])
        for vertex in self.world_vertices:
            if self.point_on_screen([vertex[0], vertex[1], vertex[2]]) == (True, True):
                p = self.project_point([vertex[0], vertex[1], vertex[2]])
                x = int(p[0])
                y = int(p[1])
                o = (vertex[2]*-1/1000) + 1
                try:
                    self.screen[y][x] = [o,o,o]
                except IndexError:
                    print("Point out of range but attempted to be rendered:", x, y)'''
        self.screen = np.zeros([self.screeny, self.screenx, 3])
        for face in self.world_faces:
            points = []
            for vertex in [self.world_vertices[face[0]], self.world_vertices[face[1]], self.world_vertices[face[2]]]:
                points_off_screen = 0
                p = self.project_point([vertex[0], vertex[1], vertex[2]])
                x = int(p[0])
                y = int(p[1])
                o = (vertex[2] * -1 / 1000) + 1
                points.append([x,y,o])
                if self.point_on_screen([vertex[0], vertex[1], vertex[2]]) != (True, True):
                    points_off_screen += 1
            if points_off_screen < 3:
                points = self.get_points_in_triangle(points[0], points[1], points[2])#
                for point in points:
                    x = int(point[0])
                    y = int(point[1])
                    o = point[2]
                    try:
                        self.screen[y][x] = [o, o, o]
                    except IndexError:
                        print("Point out of range but attempted to be rendered:", x, y)
        end = time.process_time()
        print(f"Frame time: {end-start}, Frame rate: {1/(end-start)}")
    def point_on_screen(self, position: list[float]):
        if position[2] <= 0:
            return False, False
        hfov = math.radians(self.hfov)
        vfov = math.radians(self.vfov)
        r = [math.sin(hfov / 2), 0, math.cos(hfov / 2)]
        t = [0, math.sin(vfov / 2), math.cos(vfov / 2)]
        ex = (position[2]/r[2])*r[0]
        ey = (position[2]/t[2])*t[1]
        xir = abs(position[0]) < ex
        yir = abs(position[1]) < ey
        return xir, yir
    def collapse_point(self, point: list[float]):
        x = point[0]
        y = point[1]
        z = point[2]

        x = x/z
        y = y/z
        z = 1
        return [x, y, z]
    def project_point(self, point: list[float]):
        p = self.collapse_point(point)
        x = (p[0] + 1) / 2
        y = (p[1] + 1) / 2
        x = self.screenx * x
        y = (abs(self.screeny * (1 - y)) / self.screenratio) - ((self.screenx - self.screeny) / 2)
        return x, y
    def get_points_in_triangle(self, a: list[float], b: list[float], c: list[float]):
        points = []

        ab = self.get_points_on_line(a, b)
        ac = self.get_points_on_line(c, a)
        bc = self.get_points_on_line(b, c)
        perimeter = unique_list(ab + ac + bc)
        points += perimeter

        pairs = []
        for i in range(len(perimeter)):
            for j in range(i + 1, len(perimeter)):
                if perimeter[i][0] == perimeter[j][0]:
                    pairs.append([perimeter[i], perimeter[j]])
        pairs = unique_list(pairs)
        for pair in pairs:
            points += self.get_points_on_line(pair[0], pair[1])
        return points
    def get_points_on_line(self, a: list[float], b: list[float]):
        delta = vector_subtraction(b, a)
        beta = a
        alpha = vector_division(delta, vector_size(delta))

        s = []
        for l in range(0, math.floor(vector_size(delta))):
            r = vector_addition(vector_multiplication(alpha, l), beta)
            for i in range(len(r)):
                r[i] = math.ceil(r[i])
            s.append(r)

        return unique_list(s)
