# 카레: 카메라로 찍고 레시피 추천받자! 🍛
현대인의 건강한 식습관 형성을 위한 식재료 인식 및 맞춤 레시피 추천 어플리케이션<br/><br/> 

## 🛠 재료 인식 기술 스택
<img src="https://img.shields.io/badge/yolo-00FFFF?style=for-the-badge&logo=yolo&logoColor=black"> <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"> <img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"> <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
<br><br>

## ⚙ 모델 학습
- 111개의 클래스에 해당하는 이미지 수집
- 재료 인식 모델 학습에 YOLOv5m, PyTorch 사용
- GPU를 사용하여 200 epoch 훈련

![모델 학습](https://github.com/Ottug-i/Curry_Object_Detection/assets/87821678/e753d6db-b93e-424a-b047-867940e2f4ef)
<br><br>

## 📍 모델 탑재
- Android: 1280*1280로 리사이즈한 뒤, flutter_vision 패키지를 사용해 훈련시킨 모델로 추론
- iOS: 1440*1440로 리사이즈 한 뒤, Flask로 전송하여 같은 모델로 추론

![모델 탑재](https://github.com/Ottug-i/Curry_Object_Detection/assets/87821678/7fad57ad-9647-4f25-ae50-ff3c44f8f263)
<br><br>

## 👩🏻‍💻 머신러닝 개발자
| 김가경 | 최예나 |
| :-: | :-: |
| [@GaGa-Kim](https://github.com/GaGa-Kim) | [@Choi Yena](https://github.com/YenaChoi00) |
|<img src="https://github.com/GaGa-Kim.png" style="width:150px; height:150px;">|<img src="https://avatars.githubusercontent.com/u/71956482?v=4" style="width:150px; height:150px;">|
