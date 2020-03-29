class People:
    #定义基本属性
    name = ''
    age = 0
    #定义私有属性，私有属性在类外部无法直接进行访问
    __weight = 0
    def __init__(self, n, a, w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说：我 %d岁。" %(self.name, self.age))

#单继承示例
class Student(People):
    grade = ''
    #调用父类的构造函数
    def __init__(self, n, a, w, g):
        People.__init__(self, n, a, w)
        self.grade = g
    #覆盖父类的方法
    def speak(self):
        print("%s 说：我 %d岁，我在读 %d 年级" %(self.name, self.age, self.age))

#另一个类，多重继承之前的准备
class Speaker:
    topic = ''
    name = ''
    def __init__(self, n, t):
        self.name = n
        self.topic = t
    def speak(self):
        print("我叫 %s，我是一个演说家，我演讲的主题是%s" %(self.name, self.topic))

#多重继承
class Sample(Speaker, Student):
    a = ''
    def __init__(self, n, a, w, g, t):
        Student.__init__(self, n, a, w, g)
        Speaker.__init__(self, n, t)

# 实例化类
s = Student('runoob', 10, 60, 3)
s.speak()

test = Sample('Tim', 25, 80, 4, 'Python')
test.speak()