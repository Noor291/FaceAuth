import os.path
import pickle

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import util
import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class App:
    def __init__(self):
        self.main_window = ttk.Window(themename="darkly")
        self.main_window.geometry("700x560")

        self.login_button_main_window = util.get_button(
            self.main_window, 'Check Authenticity', PRIMARY, self.login)
        self.login_button_main_window.place(x=40, y=510)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register Yourself', "PRIMARY-OUTLINE",
                                                                    self.register_new_user)
        self.register_new_user_button_main_window.place(x=375, y=510)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=20, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        #self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

    def login(self):
        name = util.recognize(self.most_recent_capture_arr, self.db_dir)
        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('ALERT!!!', 'Unknown. Please check the authenticity of the person.')
        else:
            util.msg_box('Identified!', 'Person Identified as {}.'.format(name))
            #with open(self.log_path, 'a') as f:
                #f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                #f.close()

    def register_new_user(self):
        self.register_new_user_window = ttk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("700x620")

        self.accept_button_register_new_user_window = util.get_button(
            self.register_new_user_window, 'Accept', 'SUCCESS', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=40, y=570)

        self.try_again_button_register_new_user_window = util.get_button(
            self.register_new_user_window, 'Try again', 'DANGER', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=375, y=570)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=20, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=200, y=520)

        self.text_label_register_new_user = util.get_text_label(
            self.register_new_user_window, 'Enter the name')
        self.text_label_register_new_user.place(x=40, y=520)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        embeddings = face_recognition.face_encodings(
            self.register_new_user_capture)[0]

        file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
        pickle.dump(embeddings, file)

        util.msg_box('Success!', 'User was registered successfully!')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
