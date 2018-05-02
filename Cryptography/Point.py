class Point:

    def __init__(self, x, y):
        self.__point = [x, y]

    @property
    def x(self):
        return self.__point[0]

    @property
    def y(self):
        return self.__point[1]

    @x.setter
    def x(self, value):
        self.__point[0] = value

    @y.setter
    def y(self, value):
        self.__point[1] = value



