# 1、类似私有变量，还可以定义私有方法，私有方法只能在类的内部调用，不能被外部调用

class Site:
    def __init__(self, name, url):
        self.name = name
        self.__url = url

    def who(self):
        print("name: ", self.name)
        print("url: ", self.__url)

    def __foo(self):
        print("This is private method")

    def foo(self):
        print("This is public method")
        self.__foo()


x = Site('Python', 'www.python.com')
x.who()
x.foo()
# x.__foo()       # 异常