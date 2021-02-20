from tkinter import *
from PIL import ImageTk, Image, ImageFilter
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox as mb
import traceback
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)


class App:
    def __init__(self, window, title, x, y):
        self.answer = 4
        self.canvas_w, self.canvas_h = 500, 500
        tk = window
        tk.title(title)
        tk.geometry(str(x) + "x" + str(y))
        tk.resizable(0, 0)
        tk.configure(background='white')
        self.can = Canvas(tk, width=self.canvas_w, height=self.canvas_h, bg='#edeef0', highlightthickness=0,
                          relief='ridge')
        self.can.place(x=50, y=10)
        self.current_rotate = 0
        self.current_blur = 0
        self.curr_filter = None
        self.filters = ["None","CONTOUR","DETAIL","EDGE_ENHANCE","EDGE_ENHANCE_MORE","EMBOSS","FIND_EDGES","SMOOTH","SHARPEN"]
        self.filter_label = Label(text="Filter").place(x=570,y=10)
        self.scrollbar = Scrollbar(tk)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.filter_list = Listbox(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.filter_list.yview)
        for filter in self.filters:
            self.filter_list.insert(END, filter)
        self.filter_list.place(x=570,y=30)
        self.change_filter = Button(text="Change",width=16,command=self.set_filter).place(x=570,y=200)
        self.rotate_scale = Scale(window, label='Rotate', from_=0, to=180, orient=HORIZONTAL, length=250, showvalue=0,
                                  tickinterval=20, resolution=1, command=self.rotate_image).place(x=730, y=30)
        self.blur_scale = Scale(window, label='Blur', from_=0, to=20, orient=HORIZONTAL, length=250, showvalue=0,
                                tickinterval=2, resolution=1, command=self.blur_image).place(x=730, y=100)
        self.upload = Button(text="Load image", width=20, command=self.load_img).place(x=145, y=518)
        self.save_img = Button(text="Save image", width=20, command=self.save_img).place(x=300, y=518)
        tk.mainloop()


    def update_canvas(self):
        try:
            self.curr_filter = eval(self.filter_list.get(ACTIVE))
            self.final_image = self.image.convert("RGB").filter(ImageFilter.BoxBlur(int(self.current_blur))).rotate(
                int(self.current_rotate))
            self.final_image = self.final_image.filter(self.curr_filter) if self.curr_filter is not None else self.final_image
            self.img = ImageTk.PhotoImage(self.final_image.resize((self.canvas_w, self.canvas_h)))
            self.can.create_image(20, 20, anchor=NW, image=self.img)
        except:
            mb.showerror("Error","Не удалось выполнить данное действие")

    def set_filter(self):
        self.curr_filter = eval(self.filter_list.get(ACTIVE))
        self.update_canvas()


    def blur_image(self, blur_v):
        self.current_blur = blur_v
        self.update_canvas()


    def rotate_image(self, rotate_v):
        self.current_rotate = rotate_v
        self.update_canvas()


    def load_img(self):
        self.img_path = askopenfilename()
        try:
            self.image = Image.open(self.img_path)
            self.img_width, self.img_height = self.image.size
            if ((self.img_width > self.canvas_w) or (self.img_height > self.canvas_h)):
                self.img = ImageTk.PhotoImage(self.image.resize((self.canvas_w, self.canvas_h)))
            else:
                self.img = ImageTk.PhotoImage(self.image.resize((self.canvas_w, self.canvas_h)))
            self.can.create_image(20, 20, anchor=NW, image=self.img)
            self.final_image = self.image
        except:
            pass

    def save_img(self):
        self.files = [('PNG', '*.png'),
                      ('JPEG', '*.jpg'),
                      ('All Files', '*.*')]
        self.save_path = asksaveasfile(filetypes=self.files, defaultextension=self.files)
        try:
            self.final_image.save(self.save_path.name)
            # Image.open(self.img_path).convert("RGB").filter(ImageFilter.BoxBlur(10)).save(self.save_path.name)
            # Image.open(self.img_path).resize((self.canvas_w,self.canvas_h)).crop((int(self.x1_input.get()),int(self.y1_input.get()),int(self.x2_input.get()),int(self.y2_input.get()))).save(self.save_path.name)
        except(AttributeError):
            if self.save_path:
                pass
            mb.showerror("Ошибка","Файл не найден!")

        except(ValueError):
            print(traceback.format_exc())
            mb.showerror("Ошибка", "Координаты введены неверно!")

    def l_coord(self, event):
        self.x1_input.delete(0, END)
        self.y1_input.delete(0, END)
        self.x1_input.insert(0, event.x)
        self.y1_input.insert(0, event.y)

    def r_coord(self, event):
        self.x2_input.delete(0, END)
        self.y2_input.delete(0, END)
        self.x2_input.insert(0, event.x)
        self.y2_input.insert(0, event.y)
