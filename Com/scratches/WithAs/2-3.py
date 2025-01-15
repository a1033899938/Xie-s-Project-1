class Handsomeb:

    def __enter__(self):
        print("this is 'enter' method!")
        return self

    def __exit__(self, type, value, trace):
        print("this is 'exit' method!")
        print("type: ", type)
        print("value: ", value)
        print("trace ", trace)
        return True


def cal(self):  # 创建了一个会导致异常的方法
    return 100 / 0


def get_handsomeb():
    return Handsomeb()


with get_handsomeb() as h:
    h.cal()

# 代码解析
# 我们在cal方法中创建了一段会导致异常的代码
# 在通过with调用方法get_handsomeb时，先执行对象Handsomeb中的enter方法，在执行with下的代码，发现抛出了异常
# 于是接着执行对象Handsomeb中的exit方法，过程中异常的值被赋给type、value和trace，然后被打印出来

