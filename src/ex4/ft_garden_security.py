# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Plant helpers
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Unit:
    def __init__(
        self,
        symbol: str = "",
        separator: str = " ",
        plural_s: bool = False,
    ) -> None:
        self.symbol: str = symbol
        self.separator: str = separator
        self.plural_s: bool = plural_s


CM: Unit = Unit("cm", separator="")
DAY: Unit = Unit("day", plural_s=True)
NO_UNIT: Unit = Unit(separator="")


class PlantAttr:
    def __init__(self, name: str, value, unit: Unit = NO_UNIT) -> None:
        self.name: str = name
        self.value = value
        self.unit: Unit = unit

    def get_pretty_unit(self) -> str:
        pretty_unit: str = f"{self.unit.separator}{self.unit.symbol}"
        if self.unit.plural_s and self.value != 1:
            pretty_unit += "s"
        return pretty_unit


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Plant
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self._height: PlantAttr = PlantAttr("height", round(float(height), 1), CM)
        self._age: PlantAttr = PlantAttr("age", age, DAY)
        print("Plant created: ", end="")
        self.show()

    # ~~~~~~~~ Show ~~~~~~~~
    def show(self) -> None:
        name_readout: str = f"{self.name.capitalize()}:"
        height_readout: str = f"{float(self._height.value):.1f}{self._height.get_pretty_unit()},"
        age_readout: str = f"{self._age.value}{self._age.get_pretty_unit()} old"

        print(name_readout, height_readout, age_readout)

    # ~~~~~~~~ Getters ~~~~~~~~
    def get_height(self) -> float:
        return self._get_attr("height")

    def get_age(self) -> int:
        return self._get_attr("age")

    # this and the set function generalizations are overkill,
    # but this is a learning exercise
    # and i wanted to try out __dict__
    def _get_attr(self, name: str):
        return self.__dict__["_" + name].value

    # ~~~~~~~~ Setters ~~~~~~~~

    def set_height(self, height: float) -> None:
        self._set_attr("height", round(height, 1))

    def set_age(self, age: int) -> None:
        self._set_attr("age", age)

    def _set_attr(self, name: str, value) -> None:
        if self._abort_invalid_num(name, value):
            return
        attr: PlantAttr = self.__dict__["_" + name]
        attr.value = value
        print(f"{name.capitalize()} updated: {attr.value}{attr.get_pretty_unit()}")

    def _abort_invalid_num(self, name: str, value) -> bool:
        if value < 0:
            print(f"{self.name.capitalize()}: Error, {name} can't be negative")
            print(f"{name.capitalize()} update rejected")
            return True
        return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Main
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def main() -> None:
    print("=== Garden Security System ===")

    rose: Plant = Plant("rose", 15.0, 10)
    print()

    rose.set_height(25)
    rose.set_age(30)
    print()

    rose.set_height(-5)
    rose.set_age(-3)
    print()

    print("Current state: ", end="")
    rose.show()


if __name__ == "__main__":
    main()
