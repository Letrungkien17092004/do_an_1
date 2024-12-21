from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.applications.resnet50 import preprocess_input # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
from sqlService.helper import MedicineHelper
from utilities.preprocessImage import ImagePreprocess
import tensorflow as tf
import numpy as np
import os
import json

module_dir = os.path.dirname(__file__)
class RecogniteMedicineSys:
    def __init__(self):
        self.model_link = os.path.join(module_dir, "model/medicine_recognite.keras")
        self.datas = []
        self.model = None

    def load(self):
        print()
        print("*" * 10, "loading image extract vector model", "*" * 10)
        self.model = load_model(self.model_link)
        print("*" * 10, "Done, RecogniteMedicineSys v1.0", "*" * 10)
        print()

    def loadDataFromDatabase(self):
        medicines = MedicineHelper.getAllMedicine()
        for medicine in medicines:
            if medicine.vector != "":
                self.addData(medicine.id, medicine.name, json.loads(medicine.vector))
    
    def autoTrained(self):
        medicines = MedicineHelper.getAllMedicine() # return queryset
        for medicine in medicines:
            self.updateVectorOfMedicine(medicine)

    def updateVectorOfMedicine(self, medicine):
        medicine = MedicineHelper.getById(medicineId=medicine.id)
        imagesDB = MedicineHelper.getImageOfMedicine(medicineId=medicine.id, hasTrained=False)
        for image in imagesDB:
            image = MedicineHelper.getImageById(imageId=image.id)
            image_array = ImagePreprocess.makeImageArrayInternal(image.image.url[1:])
            vectorOfImage = self.extractVector(image_array)
            if medicine.vector == "":
                medicine.vector = json.dumps(vectorOfImage.tolist())
            else:
                originVector = json.loads(medicine.vector)
                medicine.vector = json.dumps(self.combineVector(originVector, vectorOfImage).tolist())
            MedicineHelper.setImageHasTrained(imageId=image.id, hasTrained=True)
        medicine.save()

        
    def extractVector(self, image_array):
        if self.model == None: raise RuntimeError("Model is not loaded")
        preprocessedImage = preprocess_input(image_array)
        preprocessedImage = np.expand_dims(preprocessedImage, axis=0)
        vector = self.model.predict(preprocessedImage)
        return vector[0]
    
    def lookUpData(self, originVector):
        topVector = []
        for data in self.datas:
            score = self.compareVector(originVector, data["vector"])
            if score >= 0.8:
                topVector.append({
                    "id": data["id"],
                    "score": score
                })
        sorted(topVector, key=lambda data: data["score"])
        return topVector

    def compareVector(self, vectorA, vectorB):
        vector1 = tf.constant(vectorA, dtype=tf.float32)
        vector2 = tf.constant(vectorB, dtype=tf.float32)
    
        dot_product = tf.reduce_sum(vector1 * vector2)
        norm1 = tf.sqrt(tf.reduce_sum(vector1 ** 2))
        norm2 = tf.sqrt(tf.reduce_sum(vector2 ** 2))
    
        cosine_similarity = dot_product / (norm1 * norm2)
        return cosine_similarity.numpy()
    
    def combineVector(self, vectorA, vectorB):
        vectors = [
            np.array(vectorA),
            np.array(vectorB)
        ]

        combined_vector = np.mean(vectors, axis = 0)
        return combined_vector
    
    def addData(self, id, name, vector):
        index = len(self.datas)
        self.datas.append({
            "id": id,
            "name": name,
            "vector": vector,
            "index": index
        })

    def updateData(self, index, vector):
        self.datas[index].vector = vector
    
    def getData(self):
        result = []
        for data in self.datas:
            result.append({
                "id": data["id"],
                "name": data["name"],
                "index": data["index"]
            })
        return result


