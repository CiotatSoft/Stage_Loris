class Bounding_box:
    def __init__(self, name: str, x1: int, y1: int, width: int, height: int):
        self.name = name
        self.x = x1
        self.y = y1
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, x={self.x}, y={self.y}, width={self.width}, height={self.height})"


def add_collision_box(obj):
    obj.collision_box = list()
    osp = obj.sprite
    obj.collision_box.append(Bounding_box("left",
                                          osp.x, osp.y, 1, osp.height))
    obj.collision_box.append(Bounding_box("right",
                                          osp.x+osp.width-1, osp.y, 1, osp.height))
    obj.collision_box.append(Bounding_box("up",
                                          osp.x, osp.y+osp.height-1, osp.width, 1))
    obj.collision_box.append(Bounding_box("down",
                                          osp.x, osp.y, osp.width, 1))
