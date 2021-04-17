import Img
from Img import img


class ImageRecord:
    def __init__(self, imgid, image_path):
        self.id = imgid
        self.include = True
        self.image_path = image_path
        self.relpath = Img.get_image_name_from_path(self.image_path)
        self._set_caption()

    def _set_caption(self):
        the_img = self.get_the_image()
        self.caption = the_img.caption

    def get_the_image(self):
        return img(self.image_path)

    def __str__(self):
        return "img\n" + \
               "relpath:" + self.relpath + "\n" + \
               "image_path" + self.image_path + "\n"

    def __lt__(self,other):
        return self.get_the_image() < other.get_the_image()

    def __eq__(self,other):
        return self.get_the_image() == other.get_the_image()
