import numpy as np
import cv2

class Buttons:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.text_scale = 3
        self.text_thickness = 3
        self.x_margin = 20
        self.y_margin = 10

        #buttons
        self.buttons = {}
        self.button_index = 0
        self.button_area = []

        np.random.seed(0)
        self.colors = []
        self.generate_random_colors()
    def generate_random_colors(self):
        for i in range(91):
            random_color = np.random.randint(256, size=3)
            self.colors.append((int(random_color[0]), int(random_color[1]), int(random_color[2])))

    def add_buttons(self, text, x, y):
        text_size = cv2.getTextSize(text,self.font, self.text_scale, self.text_thickness)[0]
        right_x = x + (self.x_margin*2) + text_size[0]
        bottom_y = y + (self.y_margin*2) + text_size[1]
        self.buttons[self.button_index] = {"text":text,"position":[x,y,right_x,bottom_y],"active":False}
        self.button_index += 1

    def display_buttons(self,frame):
        for b_index, b_value in self.buttons.items():
            button_text = b_value["text"]
            (x,y,right_x,bottom_y) = b_value["position"]
            active_status = b_value["active"]

            if active_status :
                button_color = (0,0,200)
                text_color = (255,255,255)
                thickness = -1
            else:
                button_color = (0,0,200)
                text_color = (0,0,200)
                thickness = 3

            cv2.rectangle(frame,(x,y), (right_x,bottom_y),button_color,thickness)
            cv2.putText(frame, button_text,(x+self.x_margin , bottom_y - self.y_margin),
                        self.font,self.text_scale,text_color,self.text_thickness)
        return frame

    def button_click(self,mouse_x,mouse_y):
        for b_index, b_value in self.buttons.items():
            (x,y,right_x,bottom_y) = b_value["position"]
            active = b_value["active"]
            area = [(x,y),(right_x,y),(right_x,bottom_y),(x,bottom_y)]

            inside = cv2.pointPolygonTest(np.array(area, np.int32), (int(mouse_x), int(mouse_y)), False)
            if inside > 0:
                print("Is ac",active)
                new_status = False if active is True else True
                self.buttons[b_index]["active"] = new_status

    def active_buttons_list(self):
        active_list = []
        for b_index , b_value in self.buttons.items():
            active_status = b_value["active"]
            button_text = b_value["text"]
            if active_status:
                active_list.append(str(button_text).lower())
        return active_list

