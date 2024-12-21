from rest_framework import serializers
from PIL import Image
from tensorflow.keras.preprocessing import image # type: ignore
import base64
from io import BytesIO
import os

cwd = os.getcwd()

class ImageBase64Serializer(serializers.Serializer):
    image = serializers.CharField()

# Tôi có đoạn mã trong django python. và gặp vấn đề với kết quả của img_array
class ImagePreprocess:
    def makeImageArray(requestData):
        serializer = ImageBase64Serializer(data=requestData)
        if serializer.is_valid():
            image_data  = serializer.validated_data["image"]
            try:
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                img_data = base64.b64decode(image_data)
                img_file = BytesIO(img_data)
                pilImg = Image.open(img_file)
                pilImg = pilImg.convert('RGB')
                pilImg = pilImg.resize((224, 224))
                img_array = image.img_to_array(pilImg)
                return {
                    "success": True,
                    "image_array": img_array
                }
            except Exception as e:
                return {
                    "success": False,
                    'error': str(e)
                }
        else:
            return {
                    "success": False,
                    "error": "application/json is require"
                }
    
    def makeImageArrayInternal(url):
        imagePath = os.path.join(cwd, url)
        pilImg = Image.open(imagePath)
        pilImg = pilImg.convert('RGB')
        pilImg = pilImg.resize((224, 224))
        img_array = image.img_to_array(pilImg)
        return img_array