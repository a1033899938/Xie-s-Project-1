# 1、类似于家族中，子继承父的家族物品和佣人，类可以被继承，父类中的属性和方法都可以被子类调用
class people:  # 父类
    name = ''
    age = 0

    def __init__(self, n, a):
        self.name = n
        self.age = a

    def speak(self):
        print("%s 说：人家今年刚满　%d 岁~" % (self.name, self.age))


# 子类继承一个父类，继承多个可用class [子类]([父类]1, [父类]2, [父类]3)
class student(people):  # student为子类，people为父类
    grade = ''

    def __init__(self, n, a, g):
        # 调用父类的构函
        people.__init__(self, n, a)
        self.grade = g

    # 覆写父类的方法
    def speak(self):
        print("%s 说：人家今年刚满 %d 岁~，在读 %d 年级" % (self.name, self.age, self.grade))


s = student('ken', 18, 3)
s.speak()
