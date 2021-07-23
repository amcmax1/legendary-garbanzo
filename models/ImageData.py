from dataclasses import dataclass, field
import cv2

@dataclass(unsafe_hash=True)
class ImageData:
    uuid: str = field(init=False)
    type: str
    image_path: str
    shape: tuple = field(init=False)
    # average_color: tuple = field(init=False)
    # average_grayscale: tuple = field(init=False)
    # darkest_segment: list = field(init=False)

    def __post_init__(self):
        self.uuid = self.get_uuid()
        self.shape = self.get_shape()
        # self.average_color = self.get_average_color()
        # self.average_grayscale = self.get_average_grayscale()
        # self.darkest_segment = self.get_darkest_segment()

    def get_uuid(self) -> int:
        full_path = self.image_path.split('.')
        partial_path = full_path[0].split('/')
        return partial_path[-1]

    def get_shape(self) -> tuple:
        image = cv2.imread(self.image_path)
        return image.shape