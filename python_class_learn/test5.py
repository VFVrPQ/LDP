#定义父类
class Parent:
    def f(self):
        print ('调用父类的方法')

#定义子类
class Child(Parent):
    def f(self):
        print ('调用子类的方法')

c = Child()
c.f()
super(Child, c).f()