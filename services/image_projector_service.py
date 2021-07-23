import imageio as im
import numpy as np
import matplotlib.pyplot as plt
from modules.gnonomic_projection.nfov import NFOV


class ImageProjectorService:
    def __init__(self, er_image_path):
        self.er_image_path = er_image_path
        self.center_point = np.array([.7, .5])
        self.uuid = self.image_uuid()

    def image_uuid(self):
        full_path = self.er_image_path.split('.')
        partial_path = full_path[0].split('/')
        return partial_path[-1]

    def project_image(self):
        ed_image = im.imread(self.er_image_path)
        nfov = NFOV()
        gp_image = nfov.toNFOV(ed_image, self.center_point)
        plt.imshow(gp_image)
        plt.savefig(f'./assets/projector_images/{self.uuid}.jpg')
        plt.show()