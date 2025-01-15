class Handsomeb:

    def __enter__(self):
        print("this is 'enter' method!")
        return 'handsomeb'  # 返回了值'handsomeb'

    def __exit__(self, type, value, trace):
        print("this is 'exit' method!")


def get_handsomeb():
    return Handsomeb()


with get_handsomeb() as h:
    print("h: ", h)
# 代码解析
# 我们在enter方法中返回了值'handsomeb'，并使用“with ... as ...”的方式获取对象
# 在“with ... as ...”获取对象的方式中，可以通过as获得enter方法中的返回值
