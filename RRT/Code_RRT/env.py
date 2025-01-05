"""
RRT_2D
@author: huiming zhou

Modified by David Filliat
"""


class Env:
    def __init__(self):
        self.x_range = (0, 50)
        self.y_range = (0, 30)
        self.obs_boundary = self.obs_boundary()
        self.obs_circle = self.obs_circle()
        self.obs_rectangle = self.obs_rectangle()

    @staticmethod
    def obs_boundary():
        obs_boundary = [
            [0, 0, 1, 30],
            [0, 30, 50, 1],
            [1, 0, 50, 1],
            [50, 1, 1, 30]
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [14, 12, 8, 2],
            [18, 22, 8, 3],
            [26, 7, 2, 12],
            [32, 14, 10, 2]
        ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [
            [7, 12, 3],
            [46, 20, 2],
            [15, 5, 2],
            [37, 7, 3],
            [37, 23, 3]
        ]

        return obs_cir

class Env2:
    def __init__(self):
        self.x_range = (0, 50)
        self.y_range = (0, 30)
        self.obs_boundary = self.obs_boundary()
        self.obs_circle = self.obs_circle()
        self.obs_rectangle = self.obs_rectangle()

    @staticmethod
    def obs_boundary():
        obs_boundary = [
            [0, 0, 1, 30],
            [0, 30, 50, 1],
            [1, 0, 50, 1],
            [50, 1, 1, 30]
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [19, 1, 7, 6],
            [19, 7, 7, 6],
            [19, 13, 7, 6],
            [19, 19, 7, 6],
            [30, 7, 7, 6],
            [30, 12, 7, 6],
            [30, 18, 7, 6],
            [30, 24, 7, 6]
        ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [
                ]

        return obs_cir

class Env3:
    def __init__(self):
        self.x_range = (0, 100)
        self.y_range = (0, 60)
        self.obs_boundary = self.obs_boundary()
        self.obs_circle = self.obs_circle()
        self.obs_rectangle = self.obs_rectangle()

    @staticmethod
    def obs_boundary():
        obs_boundary = [
            [0, 0, 1, 60],
            [0, 60, 100, 1],
            [1, 0, 100, 1],
            [100, 1, 1, 60]
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [14, 12, 8, 2],
            [18, 22, 8, 3],
            [26, 7, 2, 12],
            [32, 14, 10, 2],
            [64, 12, 8, 2],
            [68, 22, 8, 3],
            [76, 7, 2, 12],
            [82, 14, 10, 2],
            [14, 42, 8, 2],
            [18, 52, 8, 3],
            [26, 37, 2, 12],
            [32, 44, 10, 2],
            [64, 42, 8, 2],
            [68, 52, 8, 3],
            [76, 37, 2, 12],
            [82, 44, 10, 2],
        ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [
            [7, 12, 3],
            [46, 20, 2],
            [15, 5, 2],
            [37, 7, 3],
            [37, 23, 3],

            [57, 12, 3],
            [96, 20, 2],
            [65, 5, 2],
            [87, 7, 3],
            [87, 23, 3],

            [7, 42, 3],
            [46, 50, 2],
            [15, 35, 2],
            [37, 37, 3],
            [37, 53, 3],

            [57, 42, 3],
            [96, 50, 2],
            [65, 35, 2],
            [87, 37, 3],
            [87, 53, 3],

        ]

        return obs_cir