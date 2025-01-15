# 类相当于于一个家族，类中的属性（即变量）相当于家族中的物品，类中的方法相当于家族中的人
# 创建一个名为Myclass的类，这个类中只有一个方法
class Myclass:

    i = 12345   # 类中的属性

    def f(self):    # 类中的方法
        return 'hello world'


x = Myclass()
print("Myclass 类的属性 i 为：", x.i)     # 类x +属性名i　= 访问属性
print("Myclass 类的方法 f 输出为：", x.f())     # 类x + 方法名f = 访问方法
