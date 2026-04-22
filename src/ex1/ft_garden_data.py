class Plant:
    def __init__(self, name: str, height_cm: int, age_days: int) -> None:
        self.name: str = name
        self.height_cm: int = height_cm
        self.age_days: int = age_days

    def show(self) -> None:
        age_unit_name: str = "day" if self.age_days == 1 else "days"
        print(
            f"{self.name.capitalize()}: {self.height_cm}cm, "
            f"{self.age_days} {age_unit_name} old"
        )


def main() -> None:
    rose: Plant = Plant("rose", 25, 30)
    sunflower: Plant = Plant("sunflower", 80, 45)
    cactus: Plant = Plant("cactus", 15, 120)

    plants: tuple[Plant, Plant, Plant] = (rose, sunflower, cactus)

    print("=== Garden Plant Registry ===")

    for p in plants:
        p.show()


if __name__ == "__main__":
    main()
