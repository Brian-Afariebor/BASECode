from __future__ import annotations

from typing import Any
from typing import Self


class Null: 

    def __repr__(self):

        return "NULL"


NULL = Null()


class Integer(int):

    @property
    def original(self):

        return super()

    def __add__(self, other: Any) -> Integer:

        return Integer(super().__add__(other))

    def __sub__(self, other: Any) -> Integer:

        return Integer(super().__sub__(other))


class Float(float):

    @property
    def original(self):

        return super()

    def __add__(self, other: Any) -> Float:

        return Float(super().__add__(other))

    def __sub__(self, other: Any) -> Float:

        return Float(super().__sub__(other))


type BASECodeLiteralString = str


class String(str):

    @staticmethod
    def from_literal(literal: BASECodeLiteralString) -> String:

        trimmed_string = literal[1:-1]

        new = (
            trimmed_string.replace(r"\n", "\n")
            .replace(r"\t", "\t")
            .replace(r"\q", '"')
            .replace(r"\\", "\\")
        )

        return String(new)

    @property
    def original(self):

        return super()

    def remove(self, string: str) -> String:

        result = self.replace(string, "")

        return String(result)

    def __add__(self, other: Any) -> String:

        return String(super().__add__(str(other)))

    def __sub__(self, other: Any) -> Self | String:

        if isinstance(other, Null):

            return self

        if isinstance(other, str):

            return self.remove(other)

        raise TypeError(
            f"""Only strings or null can be subtracted from a BASECode string;
            the type '{type(other)}' is not one of those."""
        )

    def __truediv__(self, other: Any) -> Integer | String:

        if not isinstance(other, int | float | str):

            raise TypeError(
                f"""Only strings or null can be divided from a BASECode string;
                the type '{type(other)}' is not one of those."""
            )

        if isinstance(other, str):

            return Integer(self.count(other))

        should_reverse = other < 0

        partition = abs(int(len(self) / other))

        result = self[0:partition]

        if should_reverse:

            return String(result[::-1])

        return String(result)
