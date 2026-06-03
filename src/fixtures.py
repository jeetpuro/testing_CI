class Fruit:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __eq__(self, other):
        if isinstance(other, Fruit):
            return self.name == other.name and self.color == other.color
        return False

_rec = []
_rec.append(_rec)

def recursive_func_factorial(n):
    if n == 0:
        return 1
    else:
        return n * recursive_func_factorial(n-1)
    

# Export a single dictionary of all test data
TEST_DATA = {
    "dict": {1: "I", 2: "love", 3: "Software", 4: "Testing", 5: "Pa1465", 6: "<3", 7: 1337},
    "string": "I Love Software Testing PA1465 <3",
    "int": 1337,
    "float": 2.71 + 3.14,
    "tuple": (13, 37),
    "cursed_list": [{1: "dict1", 5: "dict3"}, {1: "dict2"}, (5, 2)],
    "class_instance": Fruit("Apple", "Red"),
    "image_path": "assets/photo.png", # Path relative to project root
    "recursive list": [[2, [4,1]], [95], 8],
    "recursive_function": recursive_func_factorial(9)
}