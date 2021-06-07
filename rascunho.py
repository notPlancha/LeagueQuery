from abc import ABC, abstractmethod


class a(ABC):
    h = 0

    @abstractmethod
    def __init__(self):
        self.b = 10
        self.h = 1


class j(a):
    def init(self):
        self.h = 4

    def after(self):
        self.h = 4


print(j.h)
b = j()

print(b.h)
print(a.h)
