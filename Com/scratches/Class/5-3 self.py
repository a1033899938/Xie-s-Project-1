# 1、我们知道，一般的方法(函数)可以包含一些参数(输入)，这些参数的个数是由我们决定的
# 2、而在类中的方法却必须包含一个额外的参数，且它被放在第一个位置，它就是self
# 3、“类的实例”：也就是将类应用在实例场景中，比如类中有个方法叫f，它可以打印当天的天气，
# 假如我需要这个f来打印今天12点的天气，让它执行“打印今天12点的天气”这个动作，就叫类的实例化，
# 它让类中的方法具有的能力变成真实的动作。
class people:   #创建一个类
    # 定义类的基本属性
    name = ''
    age = 0

    # 定义类的私有属性，私有属性在类外部无法直接进行访问
    def __init__(self, n, a):
        self.name = n
        self.age = a

    def speak(self):
        print("%s 说：人家今年刚满　%d 岁~" % (self.name, self.age))


p = people('Python', 18)
# print(people.name)       #基本属性在类外部可以进行访问
# print(people.self.name)       #私有属性在类外部无法直接进行访问
p.speak()
