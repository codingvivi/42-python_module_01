class Plant:
    def __init__(self, name: str, height_cm: float, age_days: int) -> None:
        self.name: str = name
        self.height_cm: float = height_cm
        self.age_days: int = age_days

    def show(self) -> None:
        name_readout: str = f"{self.name.capitalize()}:"
        height_readout: str = f"{round(self.height_cm, 1)}cm,"
        age_unit_name: str = "day" if self.age_days == 1 else "days"
        age_readout: str = f"{self.age_days} {age_unit_name} old"

        print(name_readout, height_readout, age_readout)


def main() -> None:
    plants: tuple = (
        Plant("rose", 25.0, 30),
        Plant("oak", 200.0, 365),
        Plant("cactus", 5.0, 90),
        Plant("sunflower", 80.0, 45),
        Plant("fern", 15.0, 120),
    )

    print("=== Plant Factory Output ===")

    for plant in plants:
        print("Created: ", end="")
        plant.show()


if __name__ == "__main__":
    main()
