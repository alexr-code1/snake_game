#Import Turtle Graphics and random module
import turtle
import random 
import boto3

# define program constants
WIDTH = 800
HEIGHT = 500
DELAY = 100  # Milliseconds between screen updates
FOOD_SIZE = 20

offsets = {
    "up": (0,20),
    "down": (0,-20),
    "left": (-20,0),
    "right": (20,0)
}

def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")

def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":  # no self collision
            snake_direction = "up"
    if direction == "down":
        if snake_direction != "up":  # no self collision
            snake_direction = "down"
    if direction == "left":
        if snake_direction != "right":  # no self collision
            snake_direction = "left"
    if direction == "right":
        if snake_direction != "left":  # no self collision
            snake_direction = "right"

def move_snake():
    stamper.clearstamps()  #Remove existing stamps made by stamper
    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    #Check collisions - new head is in existing part of snake, self collision
    #x / y coordinates of new_head against boundaries of screen,calc width/heights
    if new_head in snake or new_head[0] < - WIDTH / 2 or new_head[0] > WIDTH / 2 \
       or new_head[1] < - HEIGHT /2 or new_head[1] > HEIGHT / 2:
        reset()
    else:
    
        #Add new head to snake body
        snake.append(new_head)

        #Check food collision
        if not food_collision():
            snake.pop(0)  #Keep snake same length unless fed

        #Remove last segment of snake
        #snake.pop(0)
        #Draw snake using for loop
        for segment in snake:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()

        # Refresh screen
        screen.title(f"Snake Game, Score: {score}")
        screen.update()

        #Rinse and repeat
        turtle.ontimer(move_snake, DELAY)

#if food within 20 pixels, then collision
def food_collision():
    global food_pos, score
    if get_distance(snake[-1], food_pos) < 20:
        score += 1 
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True
    return False

def get_random_food_pos():
    x = random.randint(- WIDTH / 2 + FOOD_SIZE, WIDTH / 2 - FOOD_SIZE)
    y = random.randint(- HEIGHT / 2 + FOOD_SIZE, HEIGHT / 2 - FOOD_SIZE)
    return (x,y)
def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2-y1) ** 2 + (x2-x1) **2) ** 0.5  #Pythagoras Theorem
    return distance

def reset():
    global score, snake, snake_direction, food_pos
    score = 0
    snake = [[0,0], [20,0], [40,0], [60,0]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    move_snake()

# Create a window for drawing
screen = turtle.Screen()  # Create screen
screen.setup(WIDTH, HEIGHT) #  Sets dimensions of Turtle Graphics Window.
screen.title("Snake")  # Create title
screen.bgcolor("pink")  #Set background color
screen.tracer(0) # Turns off automatic animation / more control of movement

#Event handlers
screen.listen()
bind_direction_keys()

#Create a Turtle for bidding
#Module (turtle) and class (Turtle) which represents Turtle object
stamper = turtle.Turtle()
stamper.shape("circle")
stamper.penup()

#Snake as list of lists
snake = [[0,0], [20,0], [40,0], [60,0]]
snake_direction = "up"
score = 0

#Food
food = turtle.Turtle()
food.shape("circle")
food.shapesize(FOOD_SIZE / 20)
food.penup()

# Set animation in motion
reset()

#Finish nicely
turtle.done()
