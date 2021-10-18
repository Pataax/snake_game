import random
import sys
import tkinter as tk

from PIL import Image, ImageTk


class Cons:
    BOARD_WIDTH = 300
    BOARD_HEIGHT = 300
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27


class Board(tk.Canvas):
    def __init__(self) -> None:
        super().__init__(
            width=Cons.BOARD_WIDTH,
            height=Cons.BOARD_HEIGHT,
            background="black",
            highlightthickness=0,
        )

        self.init_game()
        self.pack()

    def init_game(self):
        """initializes game"""

        self.in_game = True
        self.dots = 3
        self.score = 0

        # variables used to move snake object
        self.move_x = Cons.DOT_SIZE
        self.move_y = 0

        # starting apple coordinates
        self.apple_x = 100
        self.apple_y = 190

        self.load_images()

        self.create_objects()
        self.locate_apple()
        self.bind_all("<Key>", self.on_key_pressed)
        self.after(Cons.DELAY, self.on_timer)

    def load_images(self):
        """loads images from the disk"""

        try:
            self.i_dot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.i_dot)
            self.i_head = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.i_head)
            self.i_apple = Image.open("apple.png")
            self.apple = ImageTk.PhotoImage(self.i_apple)
        except IOError as e:
            print(e)
            sys.exit(1)

    def create_objects(self):
        """creates objects on canvas"""

        self.create_text(30, 10, text=f"Score: {self.score}", tag="score", fill="white")
        self.create_image(
            self.apple_x, self.apple_y, image=self.apple, anchor="nw", tag="apple"
        )
        self.create_image(50, 50, image=self.head, anchor="nw", tag="head")
        self.create_image(30, 50, image=self.dot, anchor="nw", tag="dot")
        self.create_image(40, 50, image=self.dot, anchor="nw", tag="dot")

    def check_apple_collision(self):
        """checks if the head of snake collides with apple"""

        apple = self.find_withtag("apple")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for over in overlap:
            if apple[0] == over:
                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.dot, anchor="nw", tag="dot")
                self.locate_apple()

    def move_snake(self):
        """moves the snake object"""

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        items = dots + head

        z = 0
        while z < len(items) - 1:
            c1 = self.coords(items[z])
            c2 = self.coords(items[z + 1])
            self.move(items[z], c2[0] - c1[0], c2[1] - c1[1])
            z += 1

        self.move(head, self.move_x, self.move_y)

    def check_collisions(self):
        """checks for collisions"""

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for dot in dots:
            for over in overlap:
                if over == dot:
                    self.in_game = False

        if x1 < 0:
            self.in_game = False

        if x1 > Cons.BOARD_HEIGHT - Cons.DOT_SIZE:
            self.in_game = False

        if y1 > Cons.BOARD_HEIGHT - Cons.DOT_SIZE:
            self.in_game = False

    def locate_apple(self):
        """places the apple object on cavas"""
        apple = self.find_withtag("apple")
        self.delete(apple[0])

        r = random.randint(0, Cons.MAX_RAND_POS)
        self.apple_x = r * Cons.DOT_SIZE
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.apple_y = r * Cons.DOT_SIZE

        self.create_image(
            self.apple_x, self.apple_y, anchor="nw", image=self.apple, tag="apple"
        )

    def on_key_pressed(self, e):
        """controls direction variables with cursor keys"""

        key = e.keysym

        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.move_x <= 0:
            self.move_x = -Cons.DOT_SIZE
            self.move_y = 0

        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.move_x >= 0:
            self.move_x = Cons.DOT_SIZE
            self.move_y = 0

        RIGHT_CURSOR_KEY = "Up"
        if key == RIGHT_CURSOR_KEY and self.move_y <= 0:
            self.move_x = 0
            self.move_y = -Cons.DOT_SIZE

        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.move_y >= 0:
            self.move_x = 0
            self.move_y = Cons.DOT_SIZE

    def on_timer(self):
        """creates a game cycle each timer event"""

        self.draw_score()
        self.check_collisions()

        if self.in_game:
            self.check_apple_collision()
            self.move_snake()
            self.after(Cons.DELAY, self.on_timer)
        else:
            self.game_over()

    def draw_score(self):
        """draws score"""

        score = self.find_withtag("score")
        self.itemconfigure(score, text=f"Score: {self.score}")

    def game_over(self):
        """deletes all objects and draws game over message"""

        self.delete(all)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game Over with score {self.score}",
            fill="white",
        )


class Snake(tk.Frame):
    def __init__(self) -> None:
        super().__init__()

        self.master.title("Snake")
        self.board = Board()
        self.pack()


def main():
    root = tk.Tk()
    nib = Snake()
    root.mainloop()


if __name__ == "__main__":
    main()
