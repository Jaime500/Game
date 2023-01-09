# Jaime McCampbell jcm2yd
"""
This is a side scrolling platform game with an animated character.
There are three separate areas of the game (the main area, a bonus area, and the winning area),
with a total of three star coin-like collectibles (hot dogs) that are hidden places.
There are three different layers that the player can travel between, a foreground, middle-ground, and
background, which help add depth to the game (pun intended) like a puzzle.
All artwork was drawn by myself and my sister Kayla McCampbell.
"""


import pygame
import gamebox
import os

GRAVITY = 1
SPEED = 6
JUMP_SPEED = 16
TOTAL_TIME = 300  # Time until the movie starts in seconds
COLORFUL = ['red', 'black', 'blue']  # These define which layers you can see at a time
BLACK = ['black']
os.chdir(os.path.dirname(__file__))


class HotDog:
    """This class creates hot dogs (to be collected)."""
    def __init__(self, x, y, color):
        self.sprite = gamebox.from_image(x, y, hot_dog_sheet[0])
        if color == 'black':
            self.sprite.image = hot_dog_sheet[1]
        elif color == 'blue':
            self.sprite.image = hot_dog_sheet[2]
        self.layer = color
        self.collected = False


camera = gamebox.Camera(800, 500)
pygame.display.set_caption('Stick Man')
pygame.display.set_icon(pygame.image.load('Stick Man Icon.png'))
skyline_sheet = gamebox.load_sprite_sheet('Skyline Sheet2.png', 3, 1)
elevator_sheet = gamebox.load_sprite_sheet('Elevator2.png', 2, 1)
bathroom_sheet = gamebox.load_sprite_sheet('Bathroom Door2.png', 3, 1)
hot_dog_sheet = gamebox.load_sprite_sheet('Hot Dog Sheet2.png', 3, 1)
stick_man_sheet = gamebox.load_sprite_sheet("Stick Man2.png", 4, 5)
stick_man = gamebox.from_image(120, 420, stick_man_sheet[0])
stick_man.speedx = 0
stick_man.speedy = 0
background = [[], []]
for n in range(-1, 8):
    background[0].append(gamebox.from_image(400 + 800 * n, 250, skyline_sheet[0]))
    background[1].append(gamebox.from_image(400 + 800 * n, 250, 'Glasses Background2.png'))
background[0][2].image = skyline_sheet[1]
background[0][4].image = skyline_sheet[2]
background[0].append(gamebox.from_color(-480, 250, (124, 124, 124), 400, 500))
background[0].append(gamebox.from_color(5490, 250, (124, 124, 124), 1380, 500))
background.append(gamebox.from_image(400, 250, 'Theater2.png'))
bathroom_background = []
for n in range(3):
    bathroom_background.extend([gamebox.from_image(5670 - 75 * n, 200, 'Sink2.png'),
                                gamebox.from_image(5430 - 80 * n, 220, 'Urinal2.png')])
    if n != 2:
        bathroom_background.append(gamebox.from_image(5100 - 175 * n, 225, 'Toilet2.png'))
layer_objects = [None,
                 {
                     'red': [
                         gamebox.from_color(2800, 480, 'red', 7200, 30),
                         gamebox.from_color(-700, 230, 'red', 40, 480),
                         gamebox.from_color(2225, 280, 'red', 150, 30),
                         gamebox.from_color(2450, 340, 'red', 10, 300),
                         gamebox.from_color(2525, 230, 'red', 150, 30),
                         gamebox.from_color(2525, 420, 'red', 150, 30),
                         gamebox.from_color(3650, 355, 'red', 150, 250),
                         gamebox.from_color(3930, 300, 'red', 30, 30),
                         gamebox.from_color(3930, 110, 'red', 30, 30),
                         gamebox.from_color(4040, 300, 'red', 30, 10),
                         gamebox.from_color(4040, 300, 'red', 30, 10),
                         gamebox.from_color(4040, 100, 'red', 30, 10),
                         gamebox.from_color(4450, 150, 'red', 60, 10),
                         gamebox.from_color(4550, 110, 'red', 10, 200),
                         gamebox.from_color(4650, 200, 'red', 60, 10),
                         gamebox.from_color(4445, 350, 'red', 88, 30),
                         gamebox.from_color(4685, 350, 'red', 88, 30),
                         gamebox.from_color(5490, 280, 'red', 1380, 30),
                         gamebox.from_color(4800, 290, 'red', 40, 350),
                         gamebox.from_color(6200, 230, 'red', 40, 480)],
                     'black': [
                         gamebox.from_color(2800, 490, 'black', 7200, 30),
                         gamebox.from_color(-700, 240, (82, 82, 82), 40, 480),
                         gamebox.from_image(1100, 380, 'Movie Box2.png'),
                         gamebox.from_color(2050, 340, 'black', 300, 30),
                         gamebox.from_color(2450, 350, 'black', 10, 300),
                         gamebox.from_color(2900, 260, 'black', 300, 30),
                         gamebox.from_color(3600, 365, 'black', 250, 250),
                         gamebox.from_color(4040, 400, 'black', 30, 10),
                         gamebox.from_color(4040, 250, 'black', 30, 10),
                         gamebox.from_color(4550, 120, 'black', 10, 200),
                         gamebox.from_color(4325, 360, 'black', 68, 30),
                         gamebox.from_color(4445, 360, 'black', 68, 30),
                         gamebox.from_color(4565, 360, 'black', 68, 30),
                         gamebox.from_color(4685, 360, 'black', 68, 30),
                         gamebox.from_color(5490, 290, 'black', 1380, 30),
                         gamebox.from_color(4800, 300, (82, 82, 82), 40, 350),
                         gamebox.from_color(6200, 240, (82, 82, 82), 40, 480)],
                     'blue': [
                         gamebox.from_color(2800, 500, 'blue', 7200, 30),
                         gamebox.from_color(-700, 250, 'blue', 40, 480),
                         gamebox.from_color(1450, 410, 'blue', 375, 30),
                         gamebox.from_color(1800, 350, 'blue', 300, 30),
                         gamebox.from_color(2450, 360, 'blue', 10, 300),
                         gamebox.from_color(2525, 340, 'blue', 150, 30),
                         gamebox.from_color(3145, 340, 'blue', 150, 30),
                         gamebox.from_color(3550, 375, 'blue', 350, 250),
                         gamebox.from_color(4040, 200, 'blue', 30, 10),
                         gamebox.from_color(4240, 100, 'blue', 30, 10),
                         gamebox.from_color(4325, 370, 'blue', 88, 30),
                         gamebox.from_color(4565, 370, 'blue', 88, 30),
                         gamebox.from_color(5490, 300, 'blue', 1380, 30),
                         gamebox.from_color(4800, 310, 'blue', 40, 350),
                         gamebox.from_color(6200, 250, 'blue', 40, 480)]
                 },
                 {
                     'red': [
                         gamebox.from_color(2800, 480, 'red', 7200, 30),
                         gamebox.from_color(5490, 280, 'red', 1380, 30),
                         gamebox.from_color(4800, 230, 'red', 40, 480),
                         gamebox.from_color(6200, 230, 'red', 40, 480),
                         gamebox.from_color(5015, 180, 'red', 10, 200),
                         gamebox.from_color(5185, 180, 'red', 10, 200),
                         gamebox.from_color(6025, 239, 'red', 10, 72),
                         gamebox.from_color(6075, 239, 'red', 10, 72)],
                     'black': [
                         gamebox.from_color(2800, 490, 'black', 7200, 30),
                         gamebox.from_color(5490, 290, 'black', 1380, 30),
                         gamebox.from_color(4800, 240, (82, 82, 82), 40, 480),
                         gamebox.from_color(6200, 240, (82, 82, 82), 40, 480),
                         gamebox.from_color(5015, 190, 'black', 10, 200),
                         gamebox.from_color(5185, 190, 'black', 10, 200),
                         gamebox.from_image(6050, 239, 'Trash Can2.png')],
                     'blue': [
                         gamebox.from_color(2800, 500, 'blue', 7200, 30),
                         gamebox.from_color(5490, 300, 'blue', 1380, 30),
                         gamebox.from_color(4800, 250, 'blue', 40, 480),
                         gamebox.from_color(6200, 250, 'blue', 40, 480)]
                 },
                 {
                     'red': [
                         gamebox.from_color(400, 495, 'red', 800, 30),
                         gamebox.from_color(-20, 230, 'red', 40, 480),
                         gamebox.from_color(820, 230, 'red', 40, 480)],
                     'black': [
                         gamebox.from_color(400, 505, 'black', 800, 30),
                         gamebox.from_color(-20, 240, (82, 82, 82), 40, 480),
                         gamebox.from_color(820, 240, (82, 82, 82), 40, 480)],
                     'blue': [
                         gamebox.from_color(400, 515, 'blue', 800, 30),
                         gamebox.from_color(-20, 250, 'blue', 40, 480),
                         gamebox.from_color(820, 250, 'blue', 40, 480)]
                 }]
portals = [None,
           [
               gamebox.from_image(-480, 380, elevator_sheet[0]),
               gamebox.from_image(5100, 180, bathroom_sheet[0]),
               gamebox.from_image(5500, 180, 'Theater Entrance2.png'),
               gamebox.from_image(5900, 180, elevator_sheet[1]),
               gamebox.from_image(5300, 395, bathroom_sheet[2]),
               gamebox.from_image(5700, 395, 'Theater Entrance2.png')],
           [gamebox.from_image(5900, 180, bathroom_sheet[1])],
           []]
end_credits = ['Directed by Jaime McCampbell', '', 'Cast:', 'Stick Man: You', 'Ticket Booth Man: Ticket Booth Man', '',
               'Set Design Team:', 'Jaime McCampbell', 'Kayla McCampbell', '',
               'No hot dogs were harmed in the making of this film.']
for n, credit in enumerate(end_credits):
    end_credits[n] = (gamebox.from_text(400, 400 + 20 * n, credit, 22, 'black'))
current_layer = 'black'
hot_dogs = [HotDog(1100, 120, 'red'), HotDog(3450, 450, 'red'), HotDog(6050, 239, 'red')]
timer_active = False
counter = 0
mobile = True
area = 0
glasses = 0
has_glasses = False
direction = 0
text = []
old_keys = []
new_keys = []
found_elevator = False
movie_over = False
win_time = 0


def initialize():
    """This function redefines everything that was just defined so that the game can restart.
    It is all repeated because pycharm didn't like it when the variables weren't defined outside the function."""
    global stick_man, current_layer, hot_dogs, timer_active, counter, mobile, area, glasses, has_glasses
    global direction, text, old_keys, new_keys, found_elevator, movie_over, win_time, end_credits
    camera.left = 0
    stick_man = gamebox.from_image(120, 420, stick_man_sheet[0])
    stick_man.speedx = 0
    stick_man.speedy = 0
    current_layer = 'black'
    hot_dogs = [HotDog(1100, 120, 'red'), HotDog(3450, 450, 'red'), HotDog(6050, 239, 'red')]
    timer_active = False
    counter = 0
    mobile = True
    area = 0
    glasses = 0
    has_glasses = False
    direction = 0
    text = []
    old_keys = []
    new_keys = []
    found_elevator = False
    movie_over = False
    win_time = 0
    end_credits = ['Directed by Jaime McCampbell', '', 'Cast:', 'Stick Man: You', 'Ticket Booth Man: Ticket Booth Man',
                   '',
                   'Set Design Team:', 'Jaime McCampbell', 'Kayla McCampbell', '',
                   'No hot dogs were harmed in the making of this film.']
    for line_number, line in enumerate(end_credits):
        end_credits[line_number] = (gamebox.from_text(400, 400 + 20 * line_number, line, 22, 'black'))


def title_screen():
    """This function displays the title screen."""
    global area
    camera.clear('white')
    camera.draw(gamebox.from_image(100, 300, 'Stick Man Title.png'))
    camera.draw(gamebox.from_text(400, 200, 'Stick Man', 80, 'black'))
    camera.draw(gamebox.from_text(400, 400, 'Move with the arrow keys', 35, 'black'))
    camera.draw(gamebox.from_text(400, 425, 'Press space to begin', 35, 'black'))
    camera.draw(gamebox.from_text(710, 490, 'Jaime McCampbell (jcm2yd)', 18, 'black'))
    camera.display()
    if pygame.K_SPACE in new_keys:
        area = 1


def hot_dog_detector():
    """This is a highly advanced function used for detecting hot dogs that have come into contact with the user
    (Stick Man)."""
    for hot_dog in hot_dogs:
        if stick_man.touches(hot_dog.sprite) and hot_dog.layer == current_layer:
            hot_dog.collected = True
            hot_dog.sprite.image = hot_dog_sheet[1]


def get_new_keys(keys):
    """This function determines which keys are newly pressed as of the current game tick."""
    global old_keys, new_keys
    new_keys = []
    for key in keys:
        if key not in old_keys:
            new_keys.append(key)
    old_keys = keys.copy()


def get_visible_layers():
    """This function determines which layers Stick Man is able to see."""
    if current_layer == 'black':
        visible_layers = BLACK
    else:
        visible_layers = COLORFUL
    return visible_layers


def stick_man_move(keys):
    """This function moves Stick Man and changes his speed depending on which keys are being pressed."""
    global direction, stick_man
    stick_man.speedy += GRAVITY
    stick_man.speedx = 0
    stick_man.image = stick_man_sheet[10 * glasses + 5 * direction]
    if (pygame.K_LEFT in keys) ^ (pygame.K_RIGHT in keys):
        if pygame.K_RIGHT in keys:
            stick_man.speedx += SPEED
            direction = 0
            stick_man.image = stick_man_sheet[10 * glasses + 5 * direction + 1 + counter // 10 % 2]
        if pygame.K_LEFT in keys:
            stick_man.speedx += -SPEED
            direction = 1
            stick_man.image = stick_man_sheet[10 * glasses + 5 * direction + 1 + counter // 10 % 2]
    stick_man.move_speed()
    for item in layer_objects[area][current_layer]:
        if stick_man.touches(item):
            stick_man.move_to_stop_overlapping(item)
            if stick_man.bottom_touches(item):
                stick_man.speedy = 0
                if pygame.K_UP in keys:
                    stick_man.speedy = -JUMP_SPEED
    if stick_man.speedy < 0:
        stick_man.image = stick_man_sheet[10 * glasses + 5 * direction + 3]
    elif stick_man.speedy > 0:
        stick_man.image = stick_man_sheet[10 * glasses + 5 * direction + 4]


def shift_layer():
    """This function shifts which layer Stick Man is in depending on which keys are being pressed."""
    global current_layer, glasses
    if (pygame.K_RSHIFT in new_keys or pygame.K_LSHIFT in new_keys) ^ (pygame.K_RCTRL in new_keys or pygame.K_LCTRL in
                                                                       new_keys):
        touching_object = False
        if pygame.K_RSHIFT in new_keys or pygame.K_LSHIFT in new_keys:
            if current_layer == 'black':
                stick_man.y -= 11
                for item in layer_objects[area]['red']:
                    if stick_man.touches(item):
                        touching_object = True
                if touching_object:
                    stick_man.y += 11
                else:
                    current_layer = 'red'
                    glasses = 1
            elif current_layer == 'blue':
                stick_man.y -= 11
                for item in layer_objects[area]['black']:
                    if stick_man.touches(item):
                        touching_object = True
                if touching_object:
                    stick_man.y += 11
                else:
                    current_layer = 'black'
                    glasses = 0
        elif pygame.K_RCTRL in new_keys or pygame.K_LCTRL in new_keys:
            if current_layer == 'red':
                stick_man.y += 9
                for item in layer_objects[area]['black']:
                    if stick_man.touches(item):
                        touching_object = True
                if touching_object:
                    stick_man.y -= 9
                else:
                    current_layer = 'black'
                    glasses = 0
            elif current_layer == 'black':
                stick_man.y += 9
                for item in layer_objects[area]['blue']:
                    if stick_man.touches(item):
                        touching_object = True
                if touching_object:
                    stick_man.y -= 9
                else:
                    current_layer = 'blue'
                    glasses = 1


def update_camera():
    """This function updates the screen."""
    if stick_man.x < camera.left + 120:
        camera.left = stick_man.x - 120
    elif stick_man.x > camera.right - 220:
        camera.right = stick_man.x + 220
    camera.clear('white')
    for item in background[glasses]:
        camera.draw(item)
    if area == 2 and current_layer == 'black':
        for item in bathroom_background:
            camera.draw(item)
    if current_layer == 'black':
        for portal in portals[area]:
            camera.draw(portal)
    layer_objects[area][current_layer].append(stick_man)
    for hot_dog in hot_dogs:
        if not hot_dog.collected:
            layer_objects[area][hot_dog.layer].append(hot_dog.sprite)
    for layer in get_visible_layers():
        for item in layer_objects[area][layer]:
            camera.draw(item)
    for i, hot_dog in enumerate(hot_dogs):
        if not hot_dog.collected:
            layer_objects[area][hot_dog.layer].pop()
        else:
            hot_dog.sprite.y = 25
            hot_dog.sprite.x = camera.left + 25 + 50 * i
            camera.draw(hot_dog.sprite)
    layer_objects[area][current_layer].pop()
    if timer_active:
        camera.draw(gamebox.from_color(camera.right - 50, 25, current_layer, 80, 36))
        if current_layer == 'black':
            color = 'grey'
        else:
            color = 'white'
        camera.draw(gamebox.from_color(camera.right - 50, 25, color, 76, 32))
        seconds = TOTAL_TIME - counter // 60
        camera.draw(gamebox.from_text(camera.right - 50, 25, '{}:{:02}'.format(seconds // 60, seconds % 60), 40,
                                      current_layer))
    if text:
        draw_text()
    # else:  # This is used to help place new things in the game.
    #     camera.draw(gamebox.from_text(camera.right - 120, 100, str(stick_man.x), 40, 'black'))
    camera.display()


def draw_text():
    """This function draws text boxes and text."""
    textbox = []
    for line_number, line in enumerate(text):
        textbox.append(gamebox.from_text(camera.left + 400, 100 + 20 * line_number, line, 22, 'black'))
    textbox_lengths = [sprite.width for sprite in textbox]
    longest = max(textbox_lengths)
    camera.draw(gamebox.from_color(camera.x, 90 + 10 * len(textbox), 'black', longest + 12, 20 * len(textbox) + 8))
    camera.draw(gamebox.from_color(camera.x, 90 + 10 * len(textbox), 'grey', longest + 8, 20 * len(textbox) + 4))
    for line in textbox:
        camera.draw(line)


def buy_movie():
    """This function handles Stick Man's interactions with Ticket Booth Man and provides Stick Man with his 3D
    glasses so that he can travel in all three dimensions."""
    global has_glasses, glasses, mobile, direction, counter, text, current_layer, timer_active
    mobile = False
    direction = 0
    stick_man_move({0})
    if camera.left < 600:
        camera.left += 60
    if glasses == 0:
        text = ["Thank you.  Here are your glasses for the movie.  It starts in 5 minutes.  Oh yeah, I'm afraid the",
                "escalators are broken right now so you'll have to find another way up to the theater.  Good luck!",
                "(press space to put on glasses)"]
    else:
        text = ["(use control and shift to travel back and forth between layers)", '(press space to continue)']
    update_camera()
    if pygame.K_SPACE in new_keys:
        if glasses == 0:
            glasses = 1
            current_layer = 'blue'
            stick_man.y += 9
        else:
            counter = 0
            timer_active = True
            has_glasses = True
            mobile = True
            text = []


def avoid_elevator():
    """This function helps make sure that Stick Man doesn't accidentally find the elevator before reaching the movie
    theater."""
    global mobile, text
    if stick_man.x <= -120 and not found_elevator:
        if stick_man.speedx == -SPEED:
            mobile = False
            stick_man.speedx = 0
            stick_man.x = -120
            if stick_man.speedy == 0:
                stick_man.image = stick_man_sheet[10 * glasses + 5 * direction]
        if pygame.K_SPACE in new_keys:
            mobile = True
        elif not mobile:
            text = ["Hmm it doesn't look like there's anything useful over there...", '(press space to continue)']


def portal_detector():
    """This function detects portals and allows Stick Man to portal through them."""
    global text, area, found_elevator, mobile
    text = []
    if area == 1:
        if current_layer == 'black':
            if stick_man.touches(portals[area][0]):
                text = ['(press space to enter the elevator)']
                if pygame.K_SPACE in new_keys:
                    stick_man.x = 5900
                    stick_man.y = 217
            elif stick_man.touches(portals[area][1]):
                text = ['(press space to enter the bathroom)']
                if pygame.K_SPACE in new_keys:
                    area = 2
                    stick_man.x += 800
            elif stick_man.touches(portals[area][2]):
                text = ['(press space to enter the theater)']
                if pygame.K_SPACE in new_keys:
                    stick_man.x = 400
                    stick_man.y = 432
                    area = 3
            elif stick_man.touches(portals[area][3]):
                if not found_elevator:
                    mobile = False
                    text = ['Wait, there was an elevator??', '(press space to continue)']
                    if pygame.K_SPACE in new_keys:
                        mobile = True
                        found_elevator = True
                else:
                    text = ['(press space to enter the elevator)']
                    if pygame.K_SPACE in new_keys:
                        stick_man.x = -480
                        stick_man.y = 417
    elif area == 2:
        if current_layer == 'black':
            if stick_man.touches(portals[area][0]):
                text = ['(press space to exit the bathroom)']
                if pygame.K_SPACE in new_keys:
                    area = 1
                    stick_man.x -= 800
    elif area == 3:
        if movie_over:
            text = ['(press space to exit the theater or enter to exit to the title screen)']
            if pygame.K_SPACE in new_keys:
                camera.x = 5500
                stick_man.x = 5500
                stick_man.y = 217
                area = 1
            elif pygame.K_RETURN in new_keys:
                initialize()


def area_1(keys):
    """This function allows Stick Man to move around and interact with the main area of the game."""
    if stick_man.bottom_touches(layer_objects[area]['black'][0]) and 895 < stick_man.x < 950 and not has_glasses:
        buy_movie()
    else:
        portal_detector()
        avoid_elevator()
        if mobile:
            stick_man_move(keys)
            if has_glasses:
                shift_layer()
            hot_dog_detector()
        update_camera()


def movie_theater(keys):
    """This function handles the end game and the cinematic masterpiece."""
    global timer_active
    global movie_over
    global win_time
    if timer_active:
        win_time = counter
    timer_active = False
    stick_man_move(keys)
    shift_layer()
    if counter % 3 == 0:
        camera.clear((250, 250, 250))
    else:
        camera.clear('white')
    camera.left = 0
    if 60 < counter - win_time < 420:
        camera.draw(gamebox.from_text(400, 125, 'Congratulations!', 60, 'black', True))
        camera.draw(gamebox.from_text(400, 200, 'You made it to the movie with ' + str(TOTAL_TIME - win_time // 60) +
                                      ' seconds left.', 30, 'black'))
        hot_dogs_collected = 0
        for i, hot_dog in enumerate(hot_dogs):
            if hot_dog.collected:
                hot_dogs_collected += 1
                hot_dog.sprite.y = 300
                hot_dog.sprite.x = camera.left + 325 + 75 * i
                camera.draw(hot_dog.sprite)
        camera.draw(gamebox.from_text(400, 250, 'You found ' + str(hot_dogs_collected) + ' of 3 hot dogs on the way.',
                                      30, 'black'))
    elif 450 < counter - win_time < 1050:
        for line in end_credits:
            line.y -= 1
            camera.draw(line)
    elif 1110 < counter - win_time:
        camera.draw(gamebox.from_text(400, 200, 'Please use the elevator to exit the theater.', 30, 'black'))
        movie_over = True
    camera.draw(background[2])
    layer_objects[area][current_layer].append(stick_man)
    for layer in get_visible_layers():
        for item in layer_objects[area][layer]:
            camera.draw(item)
    layer_objects[area][current_layer].pop()
    if text:
        draw_text()
    camera.display()
    portal_detector()


def death_screen():
    """This is a very solemn function that handles Stick Man's death.  Yes, if you miss the movie because you're bad,
    he dies."""
    camera.clear('white')
    camera.draw(gamebox.from_text(camera.left + 400, 100, 'Oh no!  You missed the movie!', 60, 'black'))
    camera.draw(gamebox.from_text(camera.left + 400, 400, '(press space to return to the title screen)', 30, 'black'))
    camera.display()
    if pygame.K_SPACE in new_keys:
        initialize()


def tick(keys):
    """This function progresses a game tick and delegates everything else."""
    global counter
    get_new_keys(keys)
    if timer_active and counter / 60 > TOTAL_TIME:
        death_screen()
    elif area == 0:
        title_screen()
    elif area == 1:
        area_1(keys)
    elif area == 2:
        area_1(keys)
    elif area == 3:
        movie_theater(keys)
    counter += 1


gamebox.timer_loop(60, tick)
