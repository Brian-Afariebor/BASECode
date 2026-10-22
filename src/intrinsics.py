from typing import Any


class Null: ...

NULL = Null()

class Integer(int): ...


class Float(float): ...


class String(str):

    def remove(self, string: str):

        result = "".join(self.split(string))

        return String(result)

    def __add__(self, other: Any):

        return super().__add__(str(other))

    def __sub__(self, other: Any):
        
        if isinstance(other, Null):
            
            return self
        
        if isinstance(other, str):
            
            return self.remove(other)

        raise NameError()

    def __truediv__(self, other: Any):

        if not isinstance(other, int | float | str):

            return other / self

        if isinstance(other, str):

            return Integer(self.count(other))

        reverse = other < 0

        partition = abs(int(len(self) / other))

        result = self[0:partition]

        if reverse:

            return String(result[::-1])

        return String(result)