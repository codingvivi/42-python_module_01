class Plant:
    def __init__(
        self, name: str, height_cm: float, age_days: int, growth_speed: float
    ) -> None:
        self.name: str = name
        self.height_cm: float = height_cm
        self.age_days: int = age_days
        self.growth_speed: float = growth_speed

    def show(self) -> None:
        name_readout: str = f"{self.name.capitalize()}:"
        height_readout: str = f"{round(self.height_cm, 1)}cm,"
        age_unit_name: str = "day" if self.age_days == 1 else "days"
        age_readout: str = f"{self.age_days} {age_unit_name} old"

        print(name_readout, height_readout, age_readout)

    def age(self, days: int) -> None:
        self.age_days += days

    def grow(
        self, days: int, growth_rates: tuple[float, ...] | None = None
    ) -> None:
        if growth_rates is None:
            growth_rates = (1.0,) * days

        for d in range(1, days + 1):
            self.age(1)
            self.height_cm += self.growth_speed * growth_rates[d - 1]


def main() -> None:

    def print_header(title: str) -> None:
        print(f"=== {title} ===")

    rose: Plant = Plant("rose", 25, 30, 0.8)

    initial_height: float = rose.height_cm

    print_header("Garden Plant Growth")
    rose.show()

    for d in range(1, 7 + 1):
        print_header(f"Day {d}")
        rose.grow(1)
        rose.show()

    growth: float = rose.height_cm - initial_height
    growth_readout: str = f"{round(growth, 1)}"

    print(f"Growth this week: {growth_readout} cm")


if __name__ == "__main__":
    main()
