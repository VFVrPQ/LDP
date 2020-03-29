class Site:
    def __init__(self, name, url):
        self.name = name #public
        self.__url = url #private
    
    def who(self):
        print('name :', self.name)
        print('url :', self.__url)

    def __foo(self):
        print('私有方法')

    def foo(self):
        print('这是共有方法')
        self.__foo()

x = Site('菜鸟教程','www.runoob.com')
x.who()
x.foo()
x.__foo() # 报错