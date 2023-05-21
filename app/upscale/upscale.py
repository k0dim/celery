import os
from bson.objectid import ObjectId
from werkzeug.datastructures import FileStorage
import numpy
from cv2 import dnn_superres
from PIL import Image
import io

from mongodb import flasc_put_file, mongo_send
from log import logger

class Upscale:

    instance = None

    def __init__(self, model_path) -> None:
        self.model_path = model_path
        self.__class__.instance = self
        logger.info(f"Create {self.__class__.__name__}")
    
    @classmethod
    def get_instance(
        cls,
        model_path = os.path.join("upscale", "model", "EDSR_x2.pb")
    ):
        if not cls.instance:
            cls.instance = cls(model_path)
        return cls.instance


    def bytes_to_pillow(self, bt: bytes):
        return Image.open(io.BytesIO(bt))


    def pillow_to_numarray(self, image):
        return numpy.asarray(image)


    def numarray_to_bytes(self, numarray: numpy.ndarray) -> bytes:
        img_crop_pil = Image.fromarray(numarray)
        byte_io = io.BytesIO()
        img_crop_pil.save(byte_io, format="png")
        jpg_buffer = byte_io.getvalue()
        byte_io.close()
        return jpg_buffer


    def scaler(self):
        scaler = dnn_superres.DnnSuperResImpl_create()
        logger.info(f"scaler: {scaler}")
        scaler.readModel(self.model_path)
        scaler.setModel("edsr", 2)
        return scaler

    
    def upscale(self, img, fname):
        logger.info(f"Start _upscale")

        scaler = dnn_superres.DnnSuperResImpl_create()
        logger.info(f"scaler: {scaler}")
        scaler.readModel(self.model_path)
        scaler.setModel("edsr", 2)
        # scaler = self.scaler()


        imagepil = self.bytes_to_pillow(img.read())
        logger.info(f"image (Image.open): {type(imagepil)}")

        imagenarray = self.pillow_to_numarray(imagepil)
        logger.info(f"image (numpy.asarray): {type(imagenarray)}")

        result = scaler.upsample(imagenarray)
        logger.info(f"result (numpy array): {type(result)}")

        result = self.numarray_to_bytes(result)
        logger.info(f"result (bytes): {type(result)}")

        result_file = FileStorage(
            filename=fname,
            stream=io.BytesIO(result)
        )

        return flasc_put_file(result_file, mongo_send)