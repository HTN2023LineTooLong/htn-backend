from ultralytics import YOLO
from PIL import Image
import glob

async def detect_people(files):
  # Load a pretrained YOLO model (recommended for training)
  model = YOLO('yolov8n.pt')

  # Perform object detection on an image using the model

  image_list = []
  # for filename in glob.glob('../uploads/*.jpg'): #assuming gif
  for file in files:
      im=Image.open(file)
      image_list.append(im)

  print('\n\n\n\nTEST\n\n\n\n')
  print(image_list)
  # Perform detection and capture the print output
  results = model.predict(source=image_list, classes=0)

  total_people = 0
  # Process results list
  for result in results:
      boxes = result.boxes
      total_people = total_people + len(boxes)

  return total_people