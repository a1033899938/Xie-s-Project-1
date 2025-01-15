class Handsomeb:  # 此对象Handsome中包含了enter和exit两个方法

    def __enter__(self):
        print("this is 'enter' method!")

    def __exit__(self, type, value, trace):
        print("this is 'exit' method!")


def get_handsomeb():  # 此方法中，执行操作为返回对象Handsomeb的值
    return Handsomeb()


with get_handsomeb():  # 用with调用方法get_Handsomeb
    print("get...")
# 代码解析
# 想要对象被with调用，对象必须包含enter和exit两个方法
# 运行时，with调用方法get_Handsomeb时，会先执行Handsomeb中的enter方法，在执行with后的代码（print("get...")），
# 最后再执行Handsomeb中的exit方法


# 临时文件2练习了"with ... as ..."调用对象的用法
# 其运行过程为：
# 1、通过with获得一个上下文管理器
# 2、执行对象
# 3、加载enter方法
# 4、加载exit方法
# 5、执行enter方法
# 6、通过as得到enter方法中的返回值
# 7、拿到对象，执行相关操作
# 8、执行结束后，执行exit方法
# 9、如果遇到异常，exit方法可以获取到异常信息
# 10、可以在exit中处理异常，比如返回True，打印异常信息等
# 11、执行with后面的语句