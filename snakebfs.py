import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
import heapq
import random

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

class SnakeGame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.grid_size = 15
        self.snake = [(0, 0)]
        self.food = (7, 5)
        self.direction = (0, 1)
        self.game_over = False
        self.path = None

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(100)

    def initUI(self):
        self.setWindowTitle("Snake Game")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        self.createBoard()

    def createBoard(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_widget = QPushButton()
                cell_widget.setStyleSheet("background-color: white;")
                cell_widget.setFixedSize(20, 20)
                self.grid_layout.addWidget(cell_widget, row, col)

    def updateGame(self):
        if not self.game_over:
            if not self.path or len(self.path) == 0:
                self.path = self.calculatePath()

            if self.path:
                next_move = self.path.pop(0)
                self.direction = (next_move[0] - self.snake[0][0], next_move[1] - self.snake[0][1])
                self.moveSnake()

                if self.snake[0] == self.food:
                    self.food = self.generateFood()
                    self.path = self.calculatePath()

                self.updateBoard()

    def moveSnake(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if new_head in self.snake or new_head[0] < 0 or new_head[0] >= self.grid_size or new_head[1] < 0 or new_head[1] >= self.grid_size:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head != self.food:
            self.snake.pop()
        else:
            self.food = self.generateFood()



    def updateBoard(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_widget = self.grid_layout.itemAtPosition(row, col).widget()
                if (row, col) in self.snake:
                    cell_widget.setStyleSheet("background-color: green;")
                elif (row, col) == self.food:
                    cell_widget.setStyleSheet("background-color: red;")
                else:
                    cell_widget.setStyleSheet("background-color: white;")

    def generateFood(self):
        while True:
            food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if food not in self.snake:
                return food
            
    def heuristic(self, neighbor):
        return abs(neighbor[0] - self.food[0]) + abs(neighbor[1] - self.food[1])

    def cost(self, neighbor):
        if (
            neighbor[0] < 0 or neighbor[0] >= self.grid_size or
            neighbor[1] < 0 or neighbor[1] >= self.grid_size or
            neighbor in self.snake
        ):
            return 10
        return 0

    def calculatePath(self):
        start = Node(self.snake[0])
        end = Node(self.food)

        queue = []
        visited = set()
        queue.append(start)

        while queue:
            current_node = queue.pop(0)

            if current_node.position == end.position:
                path = []
                while current_node.parent:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]

            if current_node.position not in visited:
                visited.add(current_node.position)

                neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for new_position in [(current_node.position[0] + d[0], current_node.position[1] + d[1]) for d in neighbors]:
                    new_node = Node(new_position, current_node)

                    if (
                        new_position[0] < 0 or new_position[0] >= self.grid_size or
                        new_position[1] < 0 or new_position[1] >= self.grid_size or
                        new_position in self.snake
                    ):
                        continue

                    queue.append(new_node)

        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec_())
