import matplotlib.pyplot as plt
import cv2


class ImageEdgeDetectionService:
    def __init__(self, er_image_path):
        self.er_image_path = er_image_path
        self.uuid = self.image_uuid()
        self.threshold = self.set_threshold()

    def set_threshold(self):
        if self.er_image_path.endswith('.png'):
            return [100, 200]
        else:
            return [100, 150]

    def image_uuid(self):
        full_path = self.er_image_path.split('.')
        partial_path = full_path[0].split('/')
        return partial_path[-1]

    def detect_edges(self):
        ed_image = cv2.imread(self.er_image_path)
        edges = cv2.Canny(ed_image, *self.threshold)
        plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        plt.savefig(f'./assets/detection_images/{self.uuid}.jpg')
        plt.show()