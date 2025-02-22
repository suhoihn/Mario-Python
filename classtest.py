class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        print(super())
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

# Example
class Spam(metaclass=Singleton):
    def __init__(self,a,b):
        print('Creating Spam')
        self.a=a
        self.b=b


if __name__ == '__main__':
    a = Spam(1,2)
    b = Spam(3,4)
    c = Spam(5,6)
    print(a.a,b.a,c.a)
    #assert a is b
