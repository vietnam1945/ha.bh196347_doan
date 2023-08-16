import cv2
import torch
import numpy as np


color = (254,226,102) 
#load model nhận diện
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True) 




#đầu vào video
image = cv2.imread("test_result.png")
frame=cv2.resize(image,(1280,800))
result = model(frame)
print(result)

# cv2.putText(frame, "1 Xe_bus", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness=2)
# cv2.putText(frame, "2 Xe_oto", (0, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness=2)
# cv2.putText(frame, "3 Xe_may", (0, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness=2)
# cv2.putText(frame, "2 Xe_tai", (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness=2)
# cv2.imshow('opening', frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()