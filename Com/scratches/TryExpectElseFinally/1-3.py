def test():
    try:
        a = 5.0 / 1.0# 除数为1，代码正常
        print("I'm try")
        return 0# 返回值为1
    except:
        print("I'm except")
        return 1
    else:# 由于try段已返回值，不执行else
        print("I'm else")
        return 2
    finally:
        print("I'm finally")
print('test: ',test())