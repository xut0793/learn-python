from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def eat(self):
        pass
    
class Dog(Animal):
    pass

if __name__ == "__main__":
    dog = Dog()
    dog.eat()