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
# Plants
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parent class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Plant:
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        growth_speed: float = 0.0,
    ) -> None:
        self.name: str = name
        self._height: PlantAttr = PlantAttr("height", 0, CM)
        self._age: PlantAttr = PlantAttr("age", 0, DAY)
        self.growth_speed: float = growth_speed
        self.set_height(height)
        self.set_age(age)
        print("Plant created: ", end="")
        self.show()

    # ~~~~~~~~ Show ~~~~~~~~
    def show(self) -> None:
        name_readout: str = f"{self.name.capitalize()}:"
        height_readout: str = f"{self._height.value}{self._height.get_pretty_unit()},"
        age_readout: str = f"{self._age.value}{self._age.get_pretty_unit()} old"

        print(name_readout, height_readout, age_readout)

    @staticmethod
    def _show_attr(attr: PlantAttr) -> None:
        print(f"{attr.name.capitalize()}: {attr.value}{attr.get_pretty_unit()}")

    # ~~~~~~~~ Getters ~~~~~~~~
    def get_height(self) -> float:
        return self._height.value

    def get_age(self) -> int:
        return self._age.value

    # ~~~~~~~~ Setters ~~~~~~~~
    def set_height(self, height: float) -> None:
        if self._abort_invalid_num("height", height):
            return
        self._height.value = round(height, 1)
        print(f"Height updated: {self._height.value}{self._height.get_pretty_unit()}")

    def set_age(self, age: int) -> None:
        if self._abort_invalid_num("age", age):
            return
        self._age.value = age
        print(f"Age updated: {self._age.value}{self._age.get_pretty_unit()}")

    @staticmethod
    def _abort_invalid_num(name: str, value: int | float) -> bool:
        if value < 0:
            print(f"Error, {name} can't be negative")
            print("Update rejected")
            return True
        return False

    # ~~~~~~~~ Lifecycle ~~~~~~~~
    def age(self, days: int) -> None:
        """aging of plant, able to be called without growth since growth of a plant can plateau"""
        self._age.value += days

    def grow(self, days: int, growth_rates=None) -> None:
        if growth_rates is None:
            growth_rates = (1.0,) * days

        for d in range(1, days + 1):
            self.age(1)
            self._height.value += self.growth_speed * growth_rates[d - 1]

    # ~~~~~~~~ Helpers for children ~~~~~~~~
    def _ask_print(
        self,
        request: str,
    ) -> None:
        print(f"[asking the {self.name} to {request}]")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Child classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Flower(Plant):
    def __init__(
        self, name: str, height: float, age: int, color: str, blooming: bool = False
    ) -> None:
        super().__init__(name, height, age)
        self.color: PlantAttr = PlantAttr("color", color)
        self.blooming: bool = blooming

    def show(self) -> None:
        super().show()
        super()._show_attr(self.color)
        if self.blooming:
            blooming_msg: str = f"{self.name.capitalize()} is blooming beautifully!"
            print(blooming_msg)

    def bloom(self):
        if self.blooming is False:
            super()._ask_print("bloom")
            self.blooming = True
        self.show()


class Tree(Plant):
    def __init__(self, name: str, height: float, age: int, diameter: float) -> None:
        super().__init__(name, height, age)
        self.diameter: PlantAttr = PlantAttr("trunk diameter", diameter, CM)

        def show(self) -> None:
            super().show()
            self._show_attr(self.diameter)

        def produce_shade(self):
            super()._ask_print("produce shade")
            print(
                f"{name} now produces a shade of {self.get_height()} long and {self.diameter} wide"
            )


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int, season: str, nutrition: int) -> None:
        super().__init__(name, height, age)
        self.harvest_season: PlantAttr = PlantAttr("harvest season", season)
        self.nutrition: PlantAttr = PlantAttr("nutritional value", nutrition)

    def grow(self, len: int):
        growth: PlantAttr = PlantAttr("grow and age", len, DAY)
        self._make_print(growth)
        super().age(growth.value)
        self._increase_nutrition(growth.value)

    def age(self, len: int):
        aging: PlantAttr = PlantAttr("age", len, DAY)
        self._make_print(aging)
        super().age(aging.value)
        self._increase_nutrition(aging.value)

    def _make_print(self, task: PlantAttr):
        print(f"[{self.name} {task.name} for {task.value}]")

    def _increase_nutrition(self, days):
        self._nutrition += 1 * days


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
