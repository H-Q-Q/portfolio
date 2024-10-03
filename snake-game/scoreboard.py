from turtle import Turtle


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.current_score = 0
        with open("snake_score.txt") as self.file:
            self.high_score = int(self.file.read())

        self.color("white")
        self.hideturtle()
        self.penup()
        self.goto(0, 280)
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Score: {self.current_score} High score: {self.high_score}", False, "center", font=('Arial', 12, 'normal'))

    def curr_score(self):
        self.current_score += 1
        self.update_score()

    def reset(self):
        if self.current_score > self.high_score:
            with open("snake_score.txt", mode='w') as self.file:
                self.file.write(str(self.current_score))
            self.high_score = self.current_score
        self.current_score = 0
        self.update_score()
