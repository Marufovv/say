# Third-party attribution

- YOLOX-S weights: OpenCV Zoo, models/object_detection_yolox/object_detection_yolox_2022nov.onnx.
  https://github.com/opencv/opencv_zoo/tree/main/models/object_detection_yolox
  Apache License 2.0, included as weights/LICENSE-YOLOX.txt.
  OpenCV Zoo contributor: Sri Siddarth Chakaravarthy (GSoC 2022); original YOLOX: Megvii-BaseDetection/YOLOX.
- src/detector.py is a locally authored adapter informed by the Apache-2.0 OpenCV Zoo yolox.py/demo.py decoding and RGB letterbox conventions; changed normalized outputs, road-user class filtering and classwise NMS.
- run_submission.py and evaluate.py: WIUT Hackathon 2026 supplied starter kit, unchanged. No upstream license was included in the supplied ZIP; their inclusion here is for the requested hackathon participation. Do not invent a license for the organizers' files.
- Python runtime dependencies: NumPy, OpenCV headless, FastAPI, Uvicorn, python-multipart. Their own licenses govern redistribution; see installed distribution metadata.
- QA used OpenCV repository samples/data/basketball1.png repeated in a synthetic 4-second video, solely to exercise real inference and upload. It is not road footage or a WIUT sample, and is not included as a project dataset.
  https://github.com/opencv/opencv/blob/master/samples/data/basketball1.png
- No model training was performed. The pretrained model was trained on COCO; original dataset image licenses vary. No additional footage from the WIUT camera was collected or scraped.
