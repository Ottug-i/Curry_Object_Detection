import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image/image.dart' as img;
import 'package:camera/camera.dart';
import 'package:image_picker/image_picker.dart';
import 'package:flutter_vision/flutter_vision.dart';

class YoloImage extends StatefulWidget {
  const YoloImage({Key? key}) : super(key: key);

  @override
  State<YoloImage> createState() => _YoloImageState();
}

class _YoloImageState extends State<YoloImage> {
  late FlutterVision vision;
  late List<Map<String, dynamic>> yoloResults;
  File? imageFile;
  int imageHeight = 1;
  int imageWidth = 1;
  bool isLoaded = false;

  late CameraController controller;
  CameraImage? cameraImage;
  bool isDetecting = false;

  @override
  void initState() {
    super.initState();
    vision = FlutterVision();
    loadYoloModel().then((value) {
      setState(() {
        yoloResults = [];
        isLoaded = true;
      });
    });
  }

  @override
  void dispose() async {
    super.dispose();
    await vision.closeYoloModel();
  }

  @override
  Widget build(BuildContext context) {
    final Size size = MediaQuery.of(context).size;
    if (!isLoaded) {
      return const Scaffold(
        body: Center(
          child: Text("Model not loaded, waiting for it"),
        ),
      );
    }
    return Stack(
      fit: StackFit.expand,
      children: [
        imageFile != null ? Image.file(imageFile!) : const SizedBox(),
        Align(
          alignment: Alignment.bottomCenter,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextButton(
                onPressed: pickImage,
                child: const Text("Pick image"),
              ),
              ElevatedButton(
                onPressed: yoloOnImage,
                child: const Text("Detect"),
              )
            ],
          ),
        ),
        ...displayBoxesAroundRecognizedObjects(size),
      ],
    );
  }

  Future<void> loadYoloModel() async {
    await vision.loadYoloModel(
        labels: 'assets/label.txt',
        modelPath: 'assets/best-1280.tflite',
        modelVersion: "yolov5",
        numThreads: 2,
        useGpu: true);
    setState(() {
      isLoaded = true;
    });
  }

  Future<void> pickImage() async {
    final ImagePicker picker = ImagePicker();
    // Capture a photo
    final XFile? photo = await picker.pickImage(source: ImageSource.gallery);
    if (photo != null) {
      setState(() {
        imageFile = File(photo.path);
      });
    }
  }

  //
  yoloOnImage() async {
    yoloResults.clear();
    Uint8List byte = await imageFile!.readAsBytes();
    // final originalImage = await decodeImageFromList(byte);

    img.Image? original = img.decodeImage(byte);

    // 이미지 크기 변경
    img.Image resized = img.copyResize(original!, width: 2560, height: 2560);
    final newByte = Uint8List.fromList(img.encodePng(resized));
    final resizedImage = await decodeImageFromList(newByte);

    imageHeight = resizedImage.height;
    imageWidth = resizedImage.width;

    final result = await vision.yoloOnImage(
        bytesList: newByte,
        imageHeight: resizedImage.height,
        imageWidth: resizedImage.width,
        iouThreshold: 0.8,
        confThreshold: 0.4,
        classThreshold: 0.7);

    if (result.isNotEmpty) {
      // 추론 결과에서 클래스 정보 추출 (중복 결과는 추가되지 않도록 코드 약간 수정 필요)
      Set<String> detectedClasses = {};
      for (var recognition in result) {
        detectedClasses.add(recognition["tag"]);
      }

      // 추론 결과 활용 (예: 클래스 정보 출력)
      // -> 결과를 사용자에게 물어보고, 필요 없는 것을 삭제한 후 백엔드 서버에 요청
      print("Detected Classes: $detectedClasses");

      setState(() {
        yoloResults = result;
      });
    }
  }

  List<Widget> displayBoxesAroundRecognizedObjects(Size screen) {
    if (yoloResults.isEmpty) return [];

    double factorX = screen.width / (imageWidth);
    double imgRatio = imageWidth / imageHeight;
    double newWidth = imageWidth * factorX;
    double newHeight = newWidth / imgRatio;
    double factorY = newHeight / (imageHeight);

    double pady = (screen.height - newHeight) / 2;

    Color colorPick = const Color.fromARGB(255, 50, 233, 30);

    return yoloResults.map((result) {
      return Positioned(
        left: result["box"][0] * factorX,
        top: result["box"][1] * factorY + pady,
        width: (result["box"][2] - result["box"][0]) * factorX,
        height: (result["box"][3] - result["box"][1]) * factorY,
        child: Container(
          decoration: BoxDecoration(
            borderRadius: const BorderRadius.all(Radius.circular(10.0)),
            border: Border.all(color: Colors.pink, width: 2.0),
          ),
          child: Text(
            "${result['tag']} ${(result['box'][4] * 100).toStringAsFixed(0)}%",
            style: TextStyle(
              background: Paint()..color = colorPick,
              color: Colors.white,
              fontSize: 18.0,
            ),
          ),
        ),
      );
    }).toList();
  }
}
