class ECpoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# parameters for our curve
a = 2
b = 3


def ECPointGen(x: int, y: int):
    """This function generates point on elliptic curve with given x and y parameters"""
    return ECpoint(x, y)


def IsOnCurveCheck(point: ECpoint):
    """This function checks whether given point is on given elliptic curve"""
    return point.y ** 3 == point.x**2 + a * point.x + b


def AddECPoints(a1: ECpoint, b1: ECpoint):
    """This function add two different points on elliptic curve and return result as point on elliptic curve"""
    m = (a1.y - b1.y) / (a1.x - b1.x)
    xr = m**2 - a1.x - b1.x
    yr = a1.y + m * (xr - a1.x)
    return ECpoint(xr, yr)


def DoubleECPoints(point: ECpoint):
    """This function adds point on elliptic curve to itself and return result as point on elliptic curve"""
    l = ((3*(point.x**2) + a) / 2*point.y)**2
    xr = l - 2*point.y
    yr = l * (point.x - xr) - point.y
    return ECpoint(xr, yr)


def ScalarMult(point: ECpoint, k: int):
    """This function defines scalar multiplication on group and returns result of k * point"""
    point_copy = point
    cnt = 1
    while k:
        if k - cnt >= 0:
            point = DoubleECPoints(point)
            cnt *= 2
            k -= cnt
        else:
            point = AddECPoints(point, point_copy)
            k -= 1
    return point


def ECPointToString(point: ECpoint):
    """This function converts elliptic curve point to string"""
    return f"P({point.x}, {point.y})"


def PrintECPoint(point: ECpoint):
    """This function prints elliptic curve point"""
    print(ECPointToString(point))


# Tests
p = ECPointGen(4, 3)
p2 = ECPointGen(-6, 3)
p_plus_p2 = AddECPoints(p, p2)
PrintECPoint(p_plus_p2)
print(IsOnCurveCheck(p))
double_p = DoubleECPoints(p)
scalar_p = ScalarMult(p, 3)
PrintECPoint(scalar_p)
p_str = ECPointToString(double_p)
PrintECPoint(double_p)
