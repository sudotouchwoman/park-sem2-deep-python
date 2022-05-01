from utils import MyShinyList


def main() -> None:
    a = MyShinyList((5, 0, -3, -1))
    b = [1] * 5

    print(a)
    print(b)

    c = a + b  # [6, 1, -2, 0, 1]
    print(c)

    is_less = b < c  # True
    print(is_less)


if __name__ == "__main__":
    main()
