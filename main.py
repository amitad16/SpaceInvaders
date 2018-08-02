# Space Invaders Part-1
import turtle
import math
import random
import pygame
import time

pygame.init()

# Setup the screen
screen = turtle.Screen()
screen.bgcolor('black')
screen.title('Space Invaders')
screen.bgpic('./assets/bg.gif')

# Register the shapes
turtle.register_shape('./assets/player.gif')
turtle.register_shape('./assets/enemy.gif')
turtle.register_shape('./assets/explosion.gif')
fire_sound = pygame.mixer.Sound('./assets/shoot.wav')
collision_sound = pygame.mixer.Sound('./assets/explosion.wav')

# Draw Border
border_pen = turtle.Turtle()
border_pen.speed(0)  # 0 means max speed
border_pen.color('white')
border_pen.penup()
border_pen.setposition(-300, -300)  # 2 arguments are x-axis and y-axis
border_pen.pensize(3)
border_pen.pendown()
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()


# Set the score
score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.penup()
score_pen.setposition(-290, 280)
score_string = 'Score : {}'.format(score)
score_pen.write(score_string, False, align='left', font=('Arial', 14, 'normal'))
score_pen.hideturtle()


# Create player turtle
player = turtle.Turtle()
player.color('blue')
player.shape('./assets/player.gif')
player.penup()
player.speed(0)
player.setposition(0, -250)
# player.setheading(90)


player_speed = 15


# Choose number of enemies
NUMBER_OF_ENEMIES = 5
# Create an empty list of enemies
enemies = []


# Add enemies to the list
for i in range(NUMBER_OF_ENEMIES):
    enemies.append(turtle.Turtle())


# Create Enenmy
for enemy in enemies:
    enemy.color('red')
    enemy.shape('./assets/enemy.gif')
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)
    enemy.setheading(270)

enemy_speed = 10


# Create the plyers bullet
p_bullet = turtle.Turtle()
p_bullet.color('yellow')
p_bullet.shape('circle')
p_bullet.penup()
p_bullet.speed(0)
p_bullet.shapesize(.5)
p_bullet.setheading(90)
p_bullet.hideturtle()
# p_bullet.setposition(player.xcor(), -245)

P_BULLET_SPEED = 30


# Define bullet state
# ready - ready to fire
# fire - bullet is firing
p_bullet_state = 'ready'


# Move the player left and right
def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -285:
        x = -285
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x > 285:
        x = 285
    player.setx(x)


def fire_bullet():
    # Declare bullet as global if it needs change
    global p_bullet_state
    if p_bullet_state == 'ready':
        pygame.mixer.Sound.play(fire_sound)
        p_bullet_state = 'fire'
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 20
        p_bullet.setposition(x, y)
        p_bullet.showturtle()


def isCollision(t1, t2):
    if t1 == player and t2 == enemy:
        for e in enemies:
            distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
            if distance < 20:
                return True
                break
            else:
                return False
    else:
        distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
        if distance < 20:
            return True
        else:
            return False


def enemy_move_left():
    x = enemy.xcor()
    x += enemy_speed
    enemy.setx(x)


def enemy_move_right():
    x = enemy.xcor()
    x -= enemy_speed
    enemy.setx(x)


def game_over():
    pygame.mixer.Sound.play(collision_sound)
    player.hideturtle()
    screen.bgpic('./assets/game over.gif')
    for e in enemies:
        e.hideturtle()


game_on = True

# Main game loop
while game_on:

    # Create keyboard binding
    turtle.onkeypress(move_left, 'Left')
    turtle.onkeypress(move_right, 'Right')
    turtle.onkey(fire_bullet, 'space')
    turtle.listen()

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 285:
            for e in enemies:
                # Move all the enemies down
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemy_speed *= -1

        if enemy.xcor() < -285:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemy_speed *= -1

        for e in enemies:
            if e.ycor() < -260:
                game_over()
                print("GAME OVER")
                game_on = False
                break

        # Check for collision between bullets and enemy
        if isCollision(p_bullet, enemy):
            pygame.mixer.Sound.play(collision_sound)
            # Reset bullet
            p_bullet.hideturtle()
            enemy.shape('./assets/explosion.gif')
            p_bullet_state = 'ready'
            p_bullet.setposition(0, -400)
            # screen.delay(50)
            enemy.shape('./assets/enemy.gif')
            # Reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            # screen.delay(0)
            # Update the score
            score += 10
            score_string = 'Score : {}'.format(score)
            score_pen.clear()
            score_pen.write(score_string, False, align='left', font=('Arial', 14, 'normal'))

        # Check collision between player and the enemy
        # Check if any enemies has come down to playes axis
        if isCollision(player, enemy):
            game_over()
            print("GAME OVER")
            game_on = False
            break

    # Move the bullet
    if p_bullet_state == 'fire':
        y = p_bullet.ycor()
        y += P_BULLET_SPEED
        p_bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if p_bullet.ycor() > 280:
        p_bullet.hideturtle()
        p_bullet_state = 'ready'


turtle.mainloop()
