class MyClass():
    """一个简单的示例"""
    i = 12345
    def f(self):
        return 'hello world'

#实例化类
x = MyClass()

# 访问类的属性和方法
print("MyClass类的属性i为：", x.i)
print("MyClass类的方法f输出为：", x.f())