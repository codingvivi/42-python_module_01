# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Plant helpers
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from typing import Any


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
        self._height: PlantAttr = PlantAttr(
            "height", round(float(height), 1), CM
        )
        self._age: PlantAttr = PlantAttr("age", age, DAY)
        self.growth_speed: float = growth_speed
        self._init_stats()
        self.show()

    class NumOf:
        def __init__(self) -> None:
            self._shows = 0
            self._agings = 0
            self._growths = 0

        def display(self) -> None:
            print(
                f"Stats: {self._growths} grow, "
                f"{self._agings} age, {self._shows} show"
            )

        def record_shade(self) -> None:
            pass

    def _init_stats(self) -> None:
        self._stats: Plant.NumOf = Plant.NumOf()

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)

    # ~~~~~~~~ Show ~~~~~~~~
    def show(self) -> None:
        name_readout: str = f"{self.name.capitalize()}:"
        height_readout: str = (
            f"{float(self._height.value):.1f}{self._height.get_pretty_unit()},"
        )
        age_readout: str = (
            f"{self._age.value}{self._age.get_pretty_unit()} old"
        )
        self._stats._shows += 1
        print(name_readout, height_readout, age_readout)

    @staticmethod
    def _show_attr(attr: PlantAttr) -> None:
        print(
            f" {attr.name.capitalize()}: {attr.value}{attr.get_pretty_unit()}"
        )

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
        print(
            f"{name.capitalize()} updated: "
            f"{attr.value}{attr.get_pretty_unit()}"
        )

    @staticmethod
    def _abort_invalid_num(name: str, value: int | float) -> bool:
        if value < 0:
            print(f"Error, {name} can't be negative")
            print("Update rejected")
            return True
        return False

    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        return age > 365

    # ~~~~~~~~ Lifecycle ~~~~~~~~
    def age(self, days: int) -> None:
        """aging of plant, able to be called without growth
        since growth of a plant can plateau"""
        if self._abort_invalid_num("days", days):
            return
        self._stats._agings += 1
        self._age.value += days

    def grow(
        self, days: int, growth_rates: tuple[float, ...] | None = None
    ) -> None:
        if growth_rates is None:
            growth_rates = (1.0,) * days
        self._stats._growths += 1
        for d in range(1, days + 1):
            self._age.value += 1
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


# ~~~~~~~~ Flower lineage ~~~~~~~~
class Flower(Plant):
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        color: str,
        blooming: bool = False,
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


class Seed(Flower):
    def __init__(
        self, name: str, height: float, age: int, color: str, seeds: int = 0
    ) -> None:
        self.seeds: PlantAttr = PlantAttr("seeds", seeds)
        super().__init__(name, height, age, color)

    def show(self) -> None:
        super().show()
        super()._show_attr(self.seeds)

    def bloom(self, seeds: int = 0) -> None:
        self.seeds.value = seeds
        super().bloom()


# ~~~~~~~~ Tree lineage ~~~~~~~~
class Tree(Plant):
    class NumOf(Plant.NumOf):
        def __init__(self) -> None:
            super().__init__()
            self._shades = 0

        def display(self) -> None:
            super().display()
            print(f" {self._shades} shade")

        def record_shade(self) -> None:
            self._shades += 1

    def __init__(
        self, name: str, height: float, age: int, diameter: float
    ) -> None:
        self.diameter: PlantAttr = PlantAttr("trunk diameter", diameter, CM)
        super().__init__(name, height, age)

    def _init_stats(self) -> None:
        self._stats = Tree.NumOf()

    def show(self) -> None:
        super().show()
        super()._show_attr(self.diameter)

    def produce_shade(self) -> None:
        self._stats.record_shade()
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

    def grow(
        self, days: int, growth_rates: tuple[float, ...] | None = None
    ) -> None:
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
        print(
            f"[make {self.name} {task.name} for "
            f"{task.value}{task.get_pretty_unit()}]"
        )

    def _increase_nutrition(self, days: int) -> None:
        self.nutrition.value += days


def display_stats(plant: Plant) -> None:
    print(f"[statistics for {plant.name.capitalize()}]")
    plant._stats.display()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Main
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def main() -> None:
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_a_year(30)}")
    print(
        f"Is 400 days more than a year? -> {Plant.is_older_than_a_year(400)}"
    )

    print("\n=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    display_stats(rose)
    rose.grow(8, (1.0,) * 8)
    rose.bloom()
    display_stats(rose)

    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    display_stats(oak)
    oak.produce_shade()
    display_stats(oak)

    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow")
    display_stats(sunflower)
    sunflower.grow(20, (1.5,) * 20)
    sunflower.age(20)
    sunflower.bloom(42)
    display_stats(sunflower)

    print("\n=== Anonymous")
    anon = Plant.anonymous()
    display_stats(anon)


if __name__ == "__main__":
    main()
