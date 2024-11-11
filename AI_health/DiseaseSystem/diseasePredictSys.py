import joblib
import json
from deep_translator import GoogleTranslator
import numpy as np
from sklearn.preprocessing import LabelBinarizer
import os
symptoms = [
    'itch',
    'skin rash',
    'nodal skin erupt',
    'sneez',
    'shiver',
    'chills',
    'joint pain',
    'stomach pain',
    'acidity',
    'ulcers on tongue',
    'muscle wasting',
    'vomit',
    'burni micturit',
    'spott urinat',
    'fatigue',
    'weight gain',
    'anxiet',
    'cold hand and feet',
    'mood swings',
    'weight loss',
    'restlessness',
    'lethargy',
    'patches in throat',
    'irregular sugar level',
    'cough',
    'high fever',
    'sunken eyes',
    'breathlessness',
    'sweat',
    'dehydrat',
    'indigest',
    'headache',
    'yellow skin',
    'dark urine',
    'nausea',
    'loss of appetite',
    'pain behind the eyes',
    'back pain',
    'constipat',
    'abdomi pain',
    'diarrhoea',
    'mild fever',
    'yellow urine',
    'yellow of eyes',
    'acute liver failure',
    'fluid overload',
    'swell of stomach',
    'swell lymph nodes',
    'malaise',
    'blurred and distorted vision',
    'phlegm',
    'throat irritat',
    'redness of eyes',
    'sinus pressure',
    'runny nose',
    'congest',
    'chest pain',
    'weakness in limbs',
    'fast heart rate',
    'pain during bowel movements',
    'pain in anal region',
    'bloody stool',
    'irritat anus',
    'neck pain',
    'dizziness',
    'cramps',
    'bruis',
    'obesit',
    'swollen leg',
    'swollen blood vessel',
    'puffy face and eye',
    'enlarged thyroid',
    'brittle nail',
    'swollen extremeties',
    'excessive hunger',
    'extra marital contacts',
    'dry and tingling lip',
    'slurr speech',
    'knee pain',
    'hip joint pain',
    'muscle weakness',
    'stiff neck',
    'swell joint',
    'movement stiffness',
    'spinning movements',
    'loss of balance',
    'unsteadiness',
    'weakness of one body side',
    'loss of smell',
    'bladder discomfort',
    'foul smell of urine',
    'continuous feel of urine',
    'passage of gases',
    'internal itch',
    'typho',
    'depression',
    'irritability',
    'muscle pain',
    'altered sensorium',
    'red spots over body',
    'belly pain',
    'abnormal menstruation',
    'dischromic  patche',
    'water eye',
    'increased appetite',
    'polyuria',
    'family history',
    'mucoid sputum',
    'rusty sputum',
    'lack concentrat',
    'visual disturbances',
    'receiv blood transfus',
    'receiv unsterile inject',
    'coma',
    'stomach bleed',
    'distent abdomen',
    'history alcohol consumpt',
    'fluid overload',
    'blood sputum',
    'prominent veins on calf',
    'palpitat',
    'pain walk',
    'pus fill pimples',
    'blackhead',
    'scurring',
    'skin peel',
    'silver like dusting',
    'small dents nail',
    'inflammatory nail',
    'blister',
    'red sore around nose',
    'yellow crust ooze'
    ]

class Translator:
    def __init__(self, source="vi", target="en"):
        self.translator = GoogleTranslator(source=source, target=target)
    def translate(self, text_vi):
        translation = self.translator.translate(text_vi)
        return translation

class DiseasePredictSys:
    def __init__(self):
        self.model_link = "./DiseaseSystem/pre_trained_model/disease_predict_tree.pkl"
        self.label_link = "./DiseaseSystem/data/classDisease.json"

        self.symptoms = symptoms
        self.model = None
        self.label = None
        self.labelBinarizer = LabelBinarizer()
        self.labelBinarizer.fit_transform(range(41))
    
    def diseasePredict(self, text_en):
        if len(text_en) <= 20: raise ValueError("text is too short")
        binarySymptom= self.getBinarySymptom(text_en)
        prediction = self.predict([binarySymptom])
        disease = self.getNameDiseaseFromPredict(prediction)
        return disease
    
    def load(self):
        self.model = joblib.load(self.model_link)
        with open(self.label_link, "r", encoding='utf-8') as f:
            self.label = json.loads(f.read())

    def getNameDiseaseFromPredict(self, prediction):
        labelNumber = self.labelBinarizer.inverse_transform(prediction)
        return self.label[labelNumber[0]]

    def predict(self, input_arr):
        input_arr = input_arr[0]
        if self.model is None: raise ValueError("the Model has not been initialized")
        if len(input_arr) != 132: raise ValueError("Array length is not accepted")

        prediction = self.model.predict([input_arr])
        print(prediction)
        return prediction
    
    def getScoreSymptom(self, symptom, text):
        items = symptom.split(" ")
        maxScore = len(items)
        score = 0
        for i in items:
            if i in text:
                score += 1
        return score / maxScore
    
    def getBinarySymptom(self, text_en):
        arr = [0] * 132
        for i in range(len(self.symptoms)):
            if self.getScoreSymptom(self.symptoms[i], text_en) >= 0.8:
                arr[i] = 1
        print("binary symptom", arr)
        return arr



