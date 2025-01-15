# 类中可以有一种特殊的人，即init()，它相当于家族中的外界联络员
# 当外界的人想调用这个家族中的人时，就必须先通过init()，即init()会先被调用
class Complex:

    def __init__(self, realpart, imagpart):     # 必须有一个self参数
        self.r = realpart
        self.i = imagpart


x = Complex(3.0, -4.5)
print(x.r, x.i)
