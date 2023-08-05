from tkinter import *
from Tetris_Figures import *
import random

class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = 400.5
        self.height = 600.5
        self.points = 0
        self.tetris_canvas = Canvas(self, width=self.width, height=self.height, borderwidth=0.5,
                                    highlightthickness=0,
                                    bg="gray")
        self.geometry(f"{401}x{700}")
        self.frame = Frame(self, width = 401, height = 100)
        self.points_label = Label(self.frame, text = f"Points: 0", font = ("Arial", 25))

        self.pause_button = Button(self.frame, text="Pause",
                                   width = 5, height = 2, command=lambda: self.stop_animation())
        self.start_button = Button(self.frame, text = "Start", width = 5, height = 2,
                                   command = self.start_game)
        self.start_button.place(x = 150, y=10)

        self.info_label = Label(self.frame, font=("Arial", 25))

        self.tetris_canvas.pack(side=BOTTOM)
        self.frame.pack(side=TOP)
        self.canvas_squares = []
        self.animation = True

    def start_game(self):
        if self.info_label["text"]=="You lost":
            self.clean_field()
            self.info_label["text"]=""
            self.points_label['text']="Points:0"
        if len(self.canvas_squares)==0:
            self.start_button.place_forget()
            self.pause_button.place(x = 150, y=10)
            self.points_label.place(x=5, y=10)
        figure_number = random.randint(1,7)
        self.figure = None
        match figure_number:
            case 1: self.figure = Square(self.tetris_canvas, self.animation, "red", 160)
            case 2:
                self.figure = JShaped(self.tetris_canvas, self.animation, "green", 160)
            case 3:
                self.figure = IShaped(self.tetris_canvas, self.animation, "yellow", 120)
            case 4:
                self.figure = TShaped(self.tetris_canvas, self.animation, "dark blue" , 160)
            case 5:
                self.figure = SShaped(self.tetris_canvas, self.animation, "pink", 160)
            case 6:
                self.figure = ZShaped(self.tetris_canvas, self.animation, "red", 120)
            case 7:
                self.figure = LShaped(self.tetris_canvas, self.animation, "purple", 160)

        if self.figure.draw()=="Stop":
            self.canvas_squares.extend(self.figure.squares)
            self.info_label.place(x=250, y=10)
            self.info_label['text'] = "You lost"
            self.pause_button.place_forget()
            self.start_button.place(x=150,y=10)
            self.points = 0
            return
        self.canvas_squares.extend(self.figure.squares)
        self.bind("<KeyPress-Right>", lambda event: self.figure.move_right(event))
        self.bind("<KeyPress-Left>", lambda event: self.figure.move_left(event))
        self.bind("<KeyPress-Up>", lambda event: self.figure.rotate(event))
        self.bind("<KeyPress-Down>", lambda event: self.figure.on_keyboard_movedown(event, 40))
        self.figure.move_down(self.figure.square_side)

        while not self.figure.move_stopped:
            self.update()

        self.unbind("<KeyPress-Right>")
        self.unbind("<KeyPress-Down>")
        self.unbind("<KeyPress-Left>")
        self.unbind("<KeyPress-Up>")
        self.delete_line(self.figure.square_side)

        self.tetris_canvas.after(500, self.start_game)

    def clean_field(self):
        self.tetris_canvas.delete("all")
        self.canvas_squares.clear()

    def delete_line(self, square_side):
        upper_bound = self.height-square_side
        lower_bound = self.height
        for i in range(int(self.height//square_side)):#!!!!
            overlapping_items = self.tetris_canvas.find_overlapping(7, upper_bound+1, self.width-1, lower_bound-1)
            if len(overlapping_items) == 10:
                for item in overlapping_items:
                    self.tetris_canvas.delete(item)
                    self.canvas_squares.remove(item)
                    self.points+=10
                self.fall_down(square_side, upper_bound)
                self.points_label["text"] = f"Points: {self.points}"
                continue
            upper_bound-=square_side
            lower_bound-=square_side

    def continue_animation(self):
        self.animation = True
        self.figure.animation_id = True
        self.continue_button.place_forget()
        self.pause_button.place(x = 150, y=10)
        self.figure.move_down(self.figure.square_side)


    def stop_animation(self):
        self.figure.animation_id=False
        self.animation = False
        self.pause_button.place_forget()
        self.continue_button = Button(self.frame, text="Continue", width = 5,height = 2,
                                      command = lambda: self.continue_animation())
        self.continue_button.place(x = 150, y=10)

    def fall_down(self, square_side, lower_bound):
        for square in self.canvas_squares:
            if self.tetris_canvas.coords(square)[3]<=lower_bound:
                self.tetris_canvas.move(square, 0, square_side)


if __name__ == '__main__':
    main_window = MainWindow()
    mainloop()
