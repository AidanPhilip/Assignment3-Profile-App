
class Parent:

    def bark(self):
        print("test")

class Child(Parent):

    def meow(self):
        print("meow")
    
test = Child()
test.bark()
test.meow()
