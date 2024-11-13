from sklearn.preprocessing import LabelEncoder
import joblib
import json
import pandas as pd
import numpy as np
import os
# Tạo đối tượng Hệ Thống Chuẩn Đoán bệnh
class DiseasePredictSys:
    # Hàm khởi tạo với các thuộc tính như bên dưới
    def __init__(self):
        self.model_link = "./DiseaseSystem/pre_trained_model/decisionTreeDisease.joblib" # tên model sẽ dùng
        self.engLabel_link = "./DiseaseSystem/data/engDisease.json" # File nhãn dữ liệu ví dụ {0: Bệnh A, 1: Bệnh B}
        self.viLabel_link = "./DiseaseSystem/data/viDisease.json" # File nhãn dữ liệu ví dụ {0: Bệnh A, 1: Bệnh B}
        self.engSymptoms_link = "./DiseaseSystem/data/engSymptoms.json" # File triệu chứng tiếng anh
        self.viSymptoms_link = "./DiseaseSystem/data/viSymptoms.json" # File triệu chứng tiếng việt
        self.model = None # Model
        self.engLabel = None # eng label
        self.viLabel = None # vie label
        self.engSymptoms = None
        self.viSymptoms = None
        self.labelEncoder = LabelEncoder() # khởi tạo đối tượng chuẩn hóa đầu ra của dữ liệu
        
    # Hàm load cần phải load trước khi có thể sử dụng bất kỳ chức năng nào của
    # hệ thống chuẩn đoán bệnh
    def debug(self):
        print(os.getcwd())
    def load(self):
        print("waiting for loading Model, data and more...")
        self.model = joblib.load(self.model_link)
        # load label
        self.engLabel = self.loadJson(self.engLabel_link)
        self.viLabel = self.loadJson(self.viLabel_link)
        self.labelEncoder.fit(self.engLabel)
        # Load symptom
        self.engSymptoms = self.loadJson(self.engSymptoms_link)
        self.viSymptoms = self.loadJson(self.viSymptoms_link)
        print("Done, DiseasePredictSys - version: v1.0")

    # Hàm đọc file json
    def loadJson(self, fileName):
        data = None
        with open(fileName, 'r', encoding = "utf-8") as f:
            data = json.loads(f.read())
        return data

    # Đây là hàm chuẩn đoán các hệ thống khác gọi đến hàm này để chuẩn đoán bệnh
    # Hàm này sẽ chuyển sang hàm chuản đoán với chat nếu người dùng chỉ định kiểu đầu vào
    # của dữ liệu là chat, ngược lại thì sẽ dùng chức năng chuẩn đoán với select
    def diseasePredict(self, raw_inp, predType):
        if (predType == "chat"):
            binary_inp = self.getBinaryText(raw_inp)
        elif predType == "select":
            binary_inp = self.getBinaryList(raw_inp)
        countImportant = self.countImportantFeature(binary_inp)
        if countImportant < 1:
            return "COUNT"
        prediction = self.predict(binary_inp)
        engDiseaseName = self.getDiseaseNameFromPrediction(prediction)
        viDiseaseName = self.getViName(engDiseaseName[0])
        return viDiseaseName

    # hàm này sẽ chuyển đổi dữ liệu đầu ra của hàm chuẩn đoán thành tên bệnh
    # vì khi chuẩn đoán tên bệnh sẽ là số vì vậy ta cần chuyển nó về chữ
    def getDiseaseNameFromPrediction(self, prediction_result):
        argMaxes = [ np.argmax(i) for i in prediction_result]
        diseaseName = self.labelEncoder.inverse_transform(argMaxes)
        return diseaseName
    # Hàm lấy tên tiếng việt từ tên tiếng anh
    def getViName(self, engName):
        for i in range(len(self.engLabel)):
            if self.engLabel[i] == engName:
                return self.viLabel[i].strip()

    # Hàm chuẩn đoán. nhận dữ liệu đàu vào là mảng các phần tử gồm 0 và 1
    # với 0 là đại diện cho không mắc triệu chứng đó và 1 là có mắc
    # kết quả sẽ là tên bệnh dưới dạng số
    def predict(self, binary_inp):
        if self.model is None: raise ValueError("the Model has not been initialized")
        binary_inp = np.array(binary_inp).reshape(1, -1)
        predict_inp = pd.DataFrame(binary_inp, columns = self.engSymptoms)
        prediction = self.model.predict_proba(predict_inp)
        return prediction

    # Hàm đếm các triệu chứng quan trọng
    # vì người dùng có thể chọn các triệu chứng như đau đầu, đau bụng...
    # các triệu chứng này không quan trọng vì nó có ở nhiều loại bệnh
    # vì vậy ta cần đếm xem người dùng cung cấp bao nhiêu triệu chứng quan trọng
    # nếu số lượng là đủ (thường là 2 triệu trứng quang trọng)
    # thì sẽ chuẩn đoán còn không thì không chuẩn đoán
    # kết quả trả về là số lượng triệu chứng quan trọng của mảng [0, 1...] đầu vào
    def countImportantFeature(self, binary_inp):
        count = 0
        for i in range(len(binary_inp)):
            if binary_inp[i] == 1:
                if self.model.feature_importances_[i] >= 0.001:
                    count += 1
        return count

    # hàm này bỏ qua không cần thêm vào báo cáo
    def getScoreSymptom(self, symptom, text_vi):
        items = symptom.split(" ")
        maxScore = len(items)
        score = 0
        for i in items:
            if i in text_vi:
                score += 1
        return score / maxScore

    # Hàm tạo ra mảng dữ liệu [0, 1, 0....] cho quá trình chuẩn đoán
    # hàm này sẽ trích xuất các tên triệu chứng và người dùng cung cấp từ tin nhắn
    # đầu vào của hàm là tin nhắn tiếng việt
    # dữ liệu trả về là mảng dữ liệu đầu vào cho qua trình chuẩn đoán tức là mảng [0, 1, 0....]
    def getBinaryText(self, text_vi):
        arr = [0] * 132
        for i in range(len(self.viSymptoms)):
            childSymptoms = self.viSymptoms[i]
            for symptom in childSymptoms:
                if self.getScoreSymptom(symptom, text_vi) >= 0.8:
                    arr[i] = 1
                    break
        return arr
        
    # Hàm này cũng tạo ra mảng dữ liệu giống hàm trên
    # khác biệt là nó sẽ trích xuất từ danh sách triệu chứng mà người dùng chọn
    # ở chế độ lựa chọn triệu chứng
    # hàm này còn đang trong giao doạn phát triển
    def getBinaryList(self, selected_list):
        binary_arr = [0] * 132
        for i in range(len(self.engSymptoms)):
            if self.engSymptoms[i] in selected_list:
                binary_arr[i] = 1
        return binary_arr