# 1、在类中可以定义私有属性，私有属性在类外部无法直接进行访问
# 定义方法是，在属性前加两条下划线。即可变为私有
class JustCounter:
    __secretCount = 0
    publicCount = 0

    def count(self):        # 方法功能为，使这两个变量+1并且打印私有变量self.__secretCount
        self.__secretCount += 1
        self.publicCount += 1
        print(self.__secretCount)


counter = JustCounter()
counter.count()
counter.count()
print(counter.publicCount)
# print(counter.__secretCount)      # 异常，实例不能访问私有变量
# 可以发现，；两次调用counter.count()的时候，counter类中的属性值的变更是会缓存的。
# 在class中声明的__secretCount = 0，publicCount = 0只生效一次，不会每次调用这个class都生效
