class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self._height: float = 0
        self._age: int = 0
        self.set_height(height)
        self.set_age(age)
        print("Plant created: ", end="")
        self.show()

    def show(self) -> None:
        name_readout: str = f"{self.name.capitalize()}:"
        height_readout: str = f"{self.get_formatted_height()},"
        age_readout: str = f"{self.get_formatted_age()} old"

        print(name_readout, height_readout, age_readout)

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def get_formatted_height(self) -> str:
        return f"{round(self.get_height(), 1)}cm"

    def get_formatted_age(self) -> str:
        value: int = self.get_age()
        unit: str = "day" if value == 1 else "days"
        return f"{value} {unit}"

    def set_height(self, height: float) -> None:
        if height < 0:
            print("Error, height can't be negative")
            print("Update rejected")
            return
        self._height = height
        print(f"Height updated: {self.get_formatted_height()}")

    def set_age(self, age: int) -> None:
        if age < 0:
            print("Error, age can't be negative")
            print("Update rejected")
            return
        self._age = age
        print(f"Age updated: {self.get_formatted_age()}")


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
