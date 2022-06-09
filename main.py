
import cv2
from  buttons_graphics import Buttons

#get nn model
net  = cv2.dnn.readNet('dnn_model/yolov4-tiny.weights', 'dnn_model/yolov4-tiny.cfg')
model = cv2.dnn_DetectionModel(net)
model.setInputParams(scale=1/255, size=(320,320), mean=None, crop=None)

#Get frames from camera
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
class_list = []

#intialize buttons
buttons = Buttons()
buttons.add_buttons("person",20,20)
buttons.add_buttons("cell phone",20,80)
buttons.add_buttons("keyboard",20,140)
buttons.add_buttons("mouse",20,200)
#create window

def on_click(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        buttons.button_click(x,y)

cv2.namedWindow("frames")
cv2.setMouseCallback("frames",on_click)
with open('dnn_model/classes.txt', 'r')  as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        class_list.append(class_name)

print("Object list")
print(class_list)

while True:
    ret , frame = cam.read()
    #object detection
    active_buttons = buttons.active_buttons_list()
    print("active buttons", active_buttons)
    (class_ids, scores, bboxes) = model.detect(frame)
    for (class_id , score, bbox) in zip(class_ids, scores, bboxes):
        (x,y,w,h) = bbox
        class_name = class_list[class_id]
        if class_name in active_buttons:
            cv2.putText(frame, str(class_list[class_id]), (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (200, 0, 50))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 0, 50), 3)
    buttons.display_buttons(frame)
    cv2.imshow("frames" , frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()