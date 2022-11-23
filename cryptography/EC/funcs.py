class ECpoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# parameters for our curve
a = 2
b = 3


def BasePointGGet():
    """This function returns base point of given elliptic curve"""
    return ECpoint(3, 6)

def ECPointGen(x: int, y: int):
    """This function generates point on elliptic curve with given x and y parameters"""
    return ECpoint(x, y)


def IsOnCurveCheck(point: ECpoint):
    """This function checks whether given point is on given elliptic curve"""
    return point.y ** 2 == point.x**3 + a * point.x + b


def AddECPoints(a1: ECpoint, b1: ECpoint):
    """This function add two different points on elliptic curve and return result as point on elliptic curve"""
    m = (a1.y - b1.y) / (a1.x - b1.x)
    xr = m**2 - a1.x - b1.x
    yr = a1.y + m * (xr - a1.x)
    return ECpoint(xr, yr)


def DoubleECPoints(point: ECpoint):
    """This function adds point on elliptic curve to itself and return result as point on elliptic curve"""
    l = (3*(point.x**2) + a) / (2*point.y)
    xr = l**2 - 2*point.x
    yr = l * (point.x - xr) - point.y
    return ECpoint(xr, yr)


def ScalarMult(point: ECpoint, k: int):
    """This function defines scalar multiplication on group and returns result of k * point"""
    point_copy = point
    if k == 1:
        return point
    else:
        point = DoubleECPoints(point)
        k -= 1
        for j in range(k - 1):
            point = AddECPoints(point, point_copy)
    return point


def ECPointToString(point: ECpoint):
    """This function converts elliptic curve point to string"""
    return f"P({point.x}, {point.y})"


def PrintECPoint(point: ECpoint):
    """This function prints elliptic curve point"""
    print(ECPointToString(point))


# Tests
if __name__ == "__main__":
    p = ECPointGen(3, 6)
    print(IsOnCurveCheck(p))
    double_p = DoubleECPoints(p)
    scalar_p = ScalarMult(p, 4)
    PrintECPoint(scalar_p)
    p_str = ECPointToString(double_p)
    PrintECPoint(double_p)
