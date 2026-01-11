# global variables
win_width = 800
win_height = 600
win_cell = round(win_width / 100)

STAR_COUNT = 5
ENEMY_COUNT = 3

left_bound = win_width / 40
right_bound = win_width - left_bound
shift = 0
speed = 0
x_start, y_start = 20, 10

# using images
img_file_back = 'static/background.jpg'
img_file_hero = 'static/unit.png'
img_file_enemy = 'static/enemy.png'
FPS = 60
GRAVITY = 0.1

# colors
C_WHITE = (255, 255, 255)
C_DARK = (48, 48, 0)
C_YELLOW = (255, 255, 87)
C_GREEN = (32, 128, 32)
C_RED = (255, 0, 0)