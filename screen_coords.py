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

def vector_cross(a: [float, float, float], b: [float, float, float]) -> [float, float, float]:
    o = [0,0,0]
    if len(a) == 2:
        a.append(0.0)
    if len(b) == 2:
        b.append(0.0)
    o[0] = a[1]*b[2] - a[2]*b[1]
    o[1] = a[2]*b[0] - a[0]*b[2]
    o[2] = a[0]*b[1] - a[1]*b[0]
    return o

def vector_dot(a: list[float], b: list[float]) -> float:
    o = 0
    for i in range(len(a)):
        o += a[i]*b[i]
    return o

def vector_lerpin(start: list[float], end: list[float], alpha: float) -> list[float]:
    diff = vector_subtraction(end, start)
    mul = vector_multiplication(diff, alpha)
    return vector_addition(start, mul)

def vector_lerpout(start: list[float], end: list[float], point: list[float]) -> float:
    t = vector_size(vector_subtraction(end, start))
    p = vector_size(vector_subtraction(point, start))
    return p / t

def lerp(start: float, end: float, alpha: float) -> float:
    return start+(end-start)*alpha

def clamp(low: float, high: float, value: float) -> float:
    return max(min(value, high), low)

class World:
    def __init__(self, screenx, screeny, fov=90.0):
        self.screenx = screenx  # screen size x
        self.screeny = screeny  # screen size y
        self.screenratio = screeny/screenx  # ratio between screen x and y
        self.hfov = fov  # horizontal fov
        self.vfov = 2 * math.degrees(math.atan(math.tan(math.radians(self.hfov/2)) * self.screenratio))  # vertical fov
        print(f"hfov: {self.hfov}   vfov: {self.vfov}   screen ratio: {self.screenratio}")

        self.screen = np.zeros([screeny, screenx, 3])  # initialise empty screen
        self.world_vertices = []  # list of vertex coordinates in 3d space
        self.world_faces = []  # list of vertexes as indexes in self.world_vertices that create a face. e.g. an element [1,4,7] means there is a face with vertexes of indexes 1, 4 and 7 in self.world_vertices
    def update_screen(self):
        start = time.process_time()  # measure frame rate
        '''
        # display only vertexes
        self.screen = np.zeros([self.screeny, self.screenx, 3])
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
        self.screen = np.zeros([self.screeny, self.screenx, 3])  # empty screen
        for face in self.world_faces:
            points = []
            for vertex in [self.world_vertices[face[0]], self.world_vertices[face[1]], self.world_vertices[face[2]]]:
                # project vertexes of each face onto screen
                points_off_screen = 0
                p = self.project_point([vertex[0], vertex[1], vertex[2]])
                x = int(p[0])
                y = int(p[1])
                o = clamp(0, 1, ((vertex[2] * -1 / 1000) + 1))  # opacity
                points.append([x,y,o])
                if self.point_on_screen([vertex[0], vertex[1], vertex[2]]) != (True, True):
                    points_off_screen += 1
            if points_off_screen < 3:  # if entire face is on screen
                points = self.get_points_in_triangle(points[0], points[1], points[2])
                for point in points:
                    x = int(point[0])
                    y = int(point[1])
                    o = point[2]
                    try:
                        self.screen[y][x] = [o, o, o]
                    except IndexError:
                        print("Point out of range but attempted to be rendered:", x, y)
        # output frame rate
        end = time.process_time()
        print(f"Frame time: {end-start}, Frame rate: {1/(end-start)}")
    def point_on_screen(self, position: list[float]):
        if position[2] <= 0:  # if point is behind camera, don't display
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
        # collapses 3d point onto plane at z = 1
        x = point[0]
        y = point[1]
        z = point[2]

        x = x/z
        y = y/z
        z = 1
        return [x, y, z]
    def project_point(self, point: list[float]):
        p = self.collapse_point(point)  # collapse point onto plane
        # adjust point range from (-,+) to (0,+)
        x = (p[0] + 1) / 2
        y = (p[1] + 1) / 2
        # expand projection to size of screen
        x = self.screenx * x
        y = (abs(self.screeny * (1 - y)) / self.screenratio) - ((self.screenx - self.screeny) / 2)
        return x, y
    def get_points_in_triangle(self, a: list[float], b: list[float], c: list[float]):
        # find range of points to search through
        max_x = math.ceil(max(a[0], b[0], c[0]))
        min_x = math.floor(min(a[0], b[0], c[0]))
        max_y = math.ceil(max(a[1], b[1], c[1]))
        min_y = math.floor(min(a[1], b[1], c[1]))

        # store vertex opacities and set to same value for easier iteration
        ao = a[2]
        bo = b[2]
        co = c[2]
        a[2] = 1.0
        b[2] = 1.0
        c[2] = 1.0

        tolerance = 0  # tolerance for determining if a point is in the triangle

        area_abc = 0.5 * vector_size(vector_cross(vector_subtraction(b, a), vector_subtraction(c, a)))

        points = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                p = [x, y, 1.0]
                # if a point is in a triangle, the sum of the areas between each vertex and the point will sum to the area of the whole triangle
                area_pab = 0.5 * vector_size(vector_cross(vector_subtraction(a, p), vector_subtraction(b, p)))
                area_pbc = 0.5 * vector_size(vector_cross(vector_subtraction(b, p), vector_subtraction(c, p)))
                area_pca = 0.5 * vector_size(vector_cross(vector_subtraction(c, p), vector_subtraction(a, p)))

                if area_abc - tolerance <= area_pab + area_pbc + area_pca <= area_abc + tolerance:  # if point is in triangle
                    # determine point opacity using a weighted average
                    pa = vector_size(vector_subtraction(a, p))
                    pb = vector_size(vector_subtraction(b, p))
                    pc = vector_size(vector_subtraction(c, p))
                    ps = pa + pb + pc

                    pa_n = 1 - (pa/ps)
                    pb_n = 1 - (pb/ps)
                    pc_n = 1 - (pc/ps)

                    p[2] = ((pa_n * ao) + (pb_n * bo) + (pc_n * co)) / (pa_n + pb_n + pc_n)

                    points.append(p)
        return points