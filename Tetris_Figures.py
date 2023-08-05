import math

class Figure:
    def __init__(self, canvas, animation_id, color, x , y = 0):
        self.canvas = canvas
        self.color = color
        self.square_side = self.canvas.winfo_reqwidth()//10
        self.squares = []
        self.x = x
        self.y = y
        self.angle_rotation = 90
        self.move_stopped = False
        # self.move_stopped.set(False)
        self.animation_id = animation_id

    def draw(self):
        for square in self.squares:
            square_coords = self.canvas.coords(square)
            overlapping_squares = list(self.canvas.find_overlapping(square_coords[0]+1,square_coords[1]+1,
                                                square_coords[2]-1,square_coords[3]-1))
            overlapping_squares.remove(square)
            if len(overlapping_squares)!=0:
                return "Stop"
            else:
                pass
        return "Continue"

    def rotate(self, event):
        if self.animation_id:
            center_x = self.x + self.square_side / 2
            center_y = self.y + self.square_side / 2
            new_coords = []
            for square in self.squares:
                x, y, _, _ = self.canvas.coords(square)
                new_x = center_x + (x - center_x) * math.cos(math.radians(self.angle_rotation)) - (y - center_y) * math.sin(
                    math.radians(self.angle_rotation))
                new_y = center_y + (x - center_x) * math.sin(math.radians(self.angle_rotation)) + (y - center_y) \
                        * math.cos(math.radians(self.angle_rotation))
                overlapping_widgets = self.canvas.find_overlapping(new_x+1, new_y+1,
                                                                   new_x + self.square_side-1, new_y + self.square_side-1)
                overlapping_widgets = set(overlapping_widgets)-set(self.squares)
                out_of_width = new_x>400 or new_x<0 or new_x+self.square_side>400 or new_x+self.square_side<0
                out_of_height = new_y>600 or new_y<0 or new_y+self.square_side>600 or new_y+self.square_side<0
                if len(overlapping_widgets)!=0 or out_of_height or out_of_width:
                    break
                new_coords.append((new_x, new_y, new_x + self.square_side, new_y + self.square_side))
            if len(new_coords)<len(self.squares):
                pass
            else:
                for i,square in enumerate(self.squares):
                    self.canvas.coords(square, new_coords[i][0], new_coords[i][1], new_coords[i][2], new_coords[i][3])

    def get_overlapping_widgets(self, x, y, width, height):
        overlapping_items = self.canvas.find_overlapping(x, y, x + width, y + height)
        overlapping_widgets = []
        overlapping_items = set(overlapping_items)-set(self.squares)
        for item_id in overlapping_items:
            bbox = self.canvas.bbox(item_id)
            item_x0, item_y0, item_x1, item_y1 = bbox
            if item_x0<=x and item_y0<=y and item_x1>=x+width and item_y1>=y+height:
                overlapping_widgets.append(item_id)
        return overlapping_widgets

    def on_keyboard_movedown(self, event, dy):
        if self.animation_id:
            for square in self.squares:
                square_coords = self.canvas.coords(square)
                overlapping_widgets = self.get_overlapping_widgets(square_coords[0],
                        square_coords[1] + self.square_side,self.square_side, self.square_side)
                if len(overlapping_widgets) != 0 or square_coords[3] == 600:
                    self.animation_id = False
                    self.move_stopped = True
                    dy = 0
            for square in self.squares:
                self.canvas.move(square, 0, dy)
            self.y += dy


    def move_down(self, dy, mlsc = 400):
        if self.animation_id:
            for square in self.squares:
                square_coords = self.canvas.coords(square)
                overlapping_widgets = self.get_overlapping_widgets(square_coords[0],
                                    square_coords[1] + self.square_side, self.square_side, self.square_side)

                if len(overlapping_widgets) != 0 or square_coords[3] == 600:
                    self.animation_id = False
                    self.move_stopped = True
                    return
            for square in self.squares:
                self.canvas.move(square, 0, dy)
            self.y += dy
            self.canvas.after(mlsc, self.move_down, dy)

    def move_right(self, event, dx = None):
        if self.animation_id:
            if dx is None:
                dx = self.square_side
            for square in self.squares:
                square_coords = self.canvas.coords(square)
                overlapping_widgets = self.get_overlapping_widgets(square_coords[0]+self.square_side,
                                                                   square_coords[1], self.square_side,
                                                                   self.square_side)
                if len(overlapping_widgets) != 0 or self.canvas.winfo_reqwidth()-square_coords[2]<40:
                    dx = 0
            for square in self.squares:
                self.canvas.move(square, dx, 0)
            self.x+=dx

    def move_left(self, event, dx = None):
        if self.animation_id:
            if dx is None:
                dx = -self.square_side
            for square in self.squares:
                square_coords = self.canvas.coords(square)
                overlapping_widgets = self.get_overlapping_widgets(square_coords[0]-self.square_side,
                                                                   square_coords[1], self.square_side,
                                                                   self.square_side)
                if len(overlapping_widgets) != 0 or square_coords[0]<40:
                    dx = 0
            for square in self.squares:
                self.canvas.move(square, dx, 0)
            self.x+=dx

class Square(Figure):
    def draw(self):
        self.squares.append(self.canvas.create_rectangle(self.x, self.y, self.x+self.square_side,
                                                         self.y+self.square_side, fill = self.color))
        self.squares.append(self.canvas.create_rectangle(self.x+self.square_side, self.y, self.x + 2*self.square_side,
                                                         self.y + self.square_side, fill=self.color))
        self.squares.append(self.canvas.create_rectangle(self.x, self.y+self.square_side, self.x + self.square_side,
                                                         self.y + 2*self.square_side, fill=self.color))
        self.squares.append(self.canvas.create_rectangle(self.x + self.square_side, self.y+self.square_side, self.x +
                                                2*self.square_side, self.y + 2*self.square_side, fill=self.color))
        return super().draw()

class LShaped(Figure):
    def draw(self):
        self.squares.append(self.canvas.create_rectangle(self.x, self.y , self.x + self.square_side,
                                                         self.y + self.square_side, fill=self.color))
        self.squares.append(self.canvas.create_rectangle(self.x, self.y + self.square_side, self.x + self.square_side,
                                                        self.y + 2 * self.square_side, fill=self.color))
        self.squares.append(self.canvas.create_rectangle(self.x + self.square_side, self.y + self.square_side, self.x +
                                                2 * self.square_side, self.y + 2 * self.square_side, fill=self.color))
        self.squares.append(self.canvas.create_rectangle(self.x + 2 * self.square_side, self.y + self.square_side,
                                            self.x + 3 * self.square_side, self.y + 2 * self.square_side, fill=self.color))
        return super().draw()

class JShaped(Figure):
    def draw(self):
        self.squares.append(self.canvas.create_rectangle(self.x, self.y+self.square_side, self.x+self.square_side,
                                                         self.y + 2*self.square_side, fill=self.color))
        self.squares.append(self.canvas.create_rectangle(self.x+self.square_side, self.y + self.square_side,
                                                         self.x + 2*self.square_side, self.y + 2 * self.square_side,
                                                         fill=self.color))
        self.squares.append(self.canvas.create_rectangle(self.x + 2*self.square_side, self.y + self.square_side,
                                                         self.x + 3 * self.square_side, self.y + 2 * self.square_side,
                                                         fill=self.color))
        self.squares.append(self.canvas.create_rectangle(self.x + 2 * self.square_side, self.y,
                                                         self.x + 3 * self.square_side, self.y + self.square_side,
                                                         fill=self.color))
        return super().draw()

class IShaped(Figure):
    def draw(self):
        for i in range(0,4):
            self.squares.append(self.canvas.create_rectangle(self.x+i*self.square_side,self.y,
                                         self.x+(i+1)*self.square_side,self.y+self.square_side, fill = self.color))
        return super().draw()

class TShaped(Figure):
    def draw(self):
        self.squares.append(self.canvas.create_rectangle(self.x , self.y,
                                                         self.x +self.square_side, self.y+self.square_side, fill=self.color))
        y = self.y + self.square_side
        x = self.x-self.square_side
        for i in range(0,3):
            self.squares.append(self.canvas.create_rectangle(x+i*self.square_side,y,
                                         x+(i+1)*self.square_side,y+self.square_side, fill = self.color))
        return super().draw()



class SShaped(Figure):
    def draw(self):
        for i in range(0,2):
            self.squares.append(self.canvas.create_rectangle(self.x+i*self.square_side,self.y,
                                        self.x+(i+1)*self.square_side,self.y+self.square_side, fill = self.color))
        for i in range(2):
            self.squares.append(self.canvas.create_rectangle(self.x - i*self.square_side, self.y + self.square_side,
                        self.x - i * self.square_side+self.square_side, self.y+2*self.square_side, fill=self.color))
        return super().draw()


class ZShaped(Figure):
    def draw(self):
        for i in range(0,2):
            self.squares.append(self.canvas.create_rectangle(self.x+i*self.square_side,self.y,
                                         self.x+(i+1)*self.square_side,self.y+self.square_side, fill = self.color))
        for i in range(1,3):
            self.squares.append(self.canvas.create_rectangle(self.x + (i)*self.square_side, self.y +self.square_side,
                                        self.x + (i+1) * self.square_side, self.y+2*self.square_side, fill=self.color))
        return super().draw()