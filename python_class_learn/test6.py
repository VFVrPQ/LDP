class JustCounter:
    __sc = 0 #私有变量
    pc = 0 #公有变量

    def count(self):
        self.__sc += 1
        self.pc += 1
        print (self.__sc)
    
counter = JustCounter()
counter.count()
counter.count()
print(counter.pc)
print(counter.__sc) #报错，示例不能访问私有变量