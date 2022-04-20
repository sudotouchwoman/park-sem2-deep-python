from utils.meta import PrefixMeta


if __name__ == "__main__":

    class SimpleCustom(metaclass=PrefixMeta):
        class_attr = 10
        also_class_attr = "string"
        __secret_value = "drowssap"

        def __init__(self, value) -> None:
            self.instance_attr = value

        def f(self, x):
            return x**2 + x

    inst = SimpleCustom(7)
    inst.new_item = {}

    print(inst.custom_new_item)
    inst.new_item = 2
    inst.instance_attr = "new value"
    print(inst.custom_new_item)

    try:
        inst.new_item
        print("Attribute found")
    except AttributeError:
        print("Attribute not found")

    print("Class vars\n", vars(SimpleCustom))
    print("Instance vars\n", vars(inst))
