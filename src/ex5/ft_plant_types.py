# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Plant helpers
#
from typing import Any

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
    def __init__(self, name: str, value: Any, unit: Unit = NO_UNIT) -> None:
        self.name: str = name
        self.value: Any = value
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
        self._height: PlantAttr = PlantAttr("height", round(float(height), 1), CM)
        self._age: PlantAttr = PlantAttr("age", age, DAY)
        self.growth_speed: float = growth_speed
        self.show()

    # ~~~~~~~~ Show ~~~~~~~~
    def show(self) -> None:
        name_readout: str = f"{self.name.capitalize()}:"
        height_readout: str = f"{float(self._height.value):.1f}{self._height.get_pretty_unit()},"
        age_readout: str = f"{self._age.value}{self._age.get_pretty_unit()} old"

        print(name_readout, height_readout, age_readout)

    # @staticmethod
    def _show_attr(self, attr: PlantAttr) -> None:
        print(f" {attr.name.capitalize()}: {attr.value}{attr.get_pretty_unit()}")

    # ~~~~~~~~ Getters ~~~~~~~~
    def get_height(self) -> float:
        height: float = self._get_attr("height")
        return height

    def get_age(self) -> int:
        age: int = self._get_attr("age")
        return age

    def _get_attr(self, name: str) -> Any:
        return self.__dict__["_" + name].value

    # ~~~~~~~~ Setters ~~~~~~~~
    def set_height(self, height: float) -> None:
        self._set_attr("height", round(height, 1))

    def set_age(self, age: int) -> None:
        self._set_attr("age", age)

    def _set_attr(self, name: str, value: Any) -> None:
        if self._abort_invalid_num(name, value):
            return
        attr: PlantAttr = self.__dict__["_" + name]
        attr.value = value
        print(f"{name.capitalize()} updated: {attr.value}{attr.get_pretty_unit()}")

    # @staticmethod
    def _abort_invalid_num(self, name: str, value: int | float) -> bool:
        if value < 0:
            print(f"Error, {name} can't be negative")
            print("Update rejected")
            return True
        return False

    # ~~~~~~~~ Lifecycle ~~~~~~~~
    def age(self, days: int) -> None:
        """aging of plant, able to be called without growth since growth of a plant can plateau"""
        self._age.value += days

    def grow(self, days: int, growth_rates: tuple[float, ...] | None = None) -> None:
        if growth_rates is None:
            growth_rates = (1.0,) * days

        for d in range(1, days + 1):
            self.age(1)
            self._height.value += self.growth_speed * growth_rates[d - 1]
        self._height.value = round(self._height.value, 1)

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
        self.color: PlantAttr = PlantAttr("color", color)
        self.blooming: bool = blooming
        super().__init__(name, height, age)

    def show(self) -> None:
        super().show()
        super()._show_attr(self.color)
        if self.blooming:
            print(f" {self.name.capitalize()} is blooming beautifully!")
        else:
            print(f" {self.name.capitalize()} has not bloomed yet")

    def bloom(self) -> None:
        if self.blooming is False:
            super()._ask_print("bloom")
            self.blooming = True
        self.show()


class Tree(Plant):
    def __init__(self, name: str, height: float, age: int, diameter: float) -> None:
        self.diameter: PlantAttr = PlantAttr("trunk diameter", diameter, CM)
        super().__init__(name, height, age)

    def show(self) -> None:
        super().show()
        super()._show_attr(self.diameter)

    def produce_shade(self) -> None:
        super()._ask_print("produce shade")
        print(
            f"Tree {self.name.capitalize()} now produces a shade of "
            f"{self.get_height()}{self.diameter.unit.symbol} long and "
            f"{self.diameter.value}{self.diameter.unit.symbol} wide."
        )


class Vegetable(Plant):
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        season: str,
        nutrition: int,
        growth_speed: float = 0.0,
    ) -> None:
        self.harvest_season: PlantAttr = PlantAttr("harvest season", season)
        self.nutrition: PlantAttr = PlantAttr("nutritional value", nutrition)
        super().__init__(name, height, age, growth_speed)

    def show(self) -> None:
        super().show()
        super()._show_attr(self.harvest_season)
        super()._show_attr(self.nutrition)

    def grow(self, days: int, growth_rates: tuple[float, ...] | None = None) -> None:
        growth: PlantAttr = PlantAttr("grow and age", days, DAY)
        self._make_print(growth)
        if growth_rates is None:
            growth_rates = (1.0,) * days
        for d in range(days):
            super().age(1)
            self._height.value += self.growth_speed * growth_rates[d]
            self._increase_nutrition(1)
        self._height.value = round(self._height.value, 1)

    def age(self, days: int) -> None:
        aging: PlantAttr = PlantAttr("age", days, DAY)
        self._make_print(aging)
        super().age(days)
        self._increase_nutrition(days)

    def _make_print(self, task: PlantAttr) -> None:
        print(f"[make {self.name} {task.name} for {task.value}{task.get_pretty_unit()}]")

    def _increase_nutrition(self, days: int) -> None:
        self.nutrition.value += days


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Main
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def main() -> None:
    print("=== Garden Plant Types ===")

    print("=== Flower")
    rose: Flower = Flower("rose", 15.0, 10, "red")
    rose.bloom()
    print()

    print("=== Tree")
    oak: Tree = Tree("oak", 200.0, 365, 5.0)
    oak.produce_shade()
    print()

    print("=== Vegetable")
    tomato: Vegetable = Vegetable("tomato", 5.0, 10, "April", 0, growth_speed=2.1)
    tomato.grow(20)
    tomato.show()


if __name__ == "__main__":
    main()
