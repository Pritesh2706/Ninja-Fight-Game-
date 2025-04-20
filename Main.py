import pygame
import time
import random
import os
import sys
import math

pygame.init()
pygame.mixer.init()

win = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Naruto vs Sasuke")

script_dir = os.path.dirname(os.path.abspath(__file__))
pics_dir = os.path.join(script_dir, 'pics')

def load_image(name):
    try:
        image = pygame.image.load(os.path.join(pics_dir, name))
        if name == 'health_potion.png':
            image = pygame.transform.scale(image, (30, 30))
        return image
    except FileNotFoundError:
        print(f"Error: Could not load image {name}")
        return pygame.Surface((100, 100))  # Fallback surface

def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join(pics_dir, name))
    except FileNotFoundError:
        print(f"Error: Could not load sound {name}")
        return None

# GIF animation support for front.gif
class GifAnimation:
    def __init__(self, filename, frame_count=10, frame_duration=0.1):
        self.frames = []
        self.frame_count = frame_count
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_frame_time = time.time()
        try:
            base_image = load_image(filename)
            frame_width = base_image.get_width() // frame_count
            for i in range(frame_count):
                frame = base_image.subsurface((i * frame_width, 0, frame_width, base_image.get_height()))
                self.frames.append(frame)
        except Exception as e:
            print(f"Error loading GIF: {e}")
            # Fallback to a static background
            fallback_image = load_image('front 2.jpg')  # Use bg1.png as fallback
            self.frames = [pygame.transform.scale(fallback_image, (700, 500))]
    def get_current_frame(self):
        if time.time() - self.last_frame_time >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_time = time.time()
        return self.frames[self.current_frame]

walkRight = [load_image('NR2.png'), load_image('NR3.png'), load_image('NR1.png')]
walkLeft = [load_image('NL2.png'), load_image('NL3.png'), load_image('NL1.png')]
backgrounds = ['bg1.png', 'bg2.png', 'bg3.png', 'bg4.png']
current_bg = random.choice(backgrounds)
bg = load_image(current_bg)
Nh = load_image('Nh.png')
Sh = load_image('Sh.png')
naruto_dead = load_image('Nd.png')
sasuke_dead = load_image('Sd.png')
shuriken_img = load_image('shur.png')
health_potion_img = load_image('health_potion.png')

hitSound = load_sound('hit.wav')
sound_enabled = True
try:
    pygame.mixer.music.load(os.path.join(pics_dir, 'naruto_mix.mp3'))
    pygame.mixer.music.play(-1)
except:
    print("Error: Could not load background music")

Clock = pygame.time.Clock()

font_large = pygame.font.SysFont('comicsans', 80, True)
font_medium = pygame.font.SysFont('comicsans', 60, True)
font_small = pygame.font.SysFont('comicsans', 40, True)
font_very_small = pygame.font.SysFont('comicsans', 20, True)
font_level = pygame.font.SysFont('comicsans', 30, True)
font_pause = pygame.font.SysFont('comicsans', 20, True)

PROGRESS_FILE = os.path.join(script_dir, 'progress.txt')

def save_progress(level):
    with open(PROGRESS_FILE, 'w') as f:
        f.write(str(level))

def load_progress():
    try:
        with open(PROGRESS_FILE, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 1

class HealthPotion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.hitbox = (self.x + 15 - 15, self.y + 15 - 15, 30, 30)
        self.collected = False
    def draw(self, win):
        if not self.collected:
            win.blit(health_potion_img, (self.x, self.y))
            self.hitbox = (self.x + 15 - 15, self.y + 15 - 15, 30, 30)

class player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.isjump = False
        self.jumpheight = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        self.health = 200
        self.max_health = 200
    def draw(self, win, naruto_wins=False, sasuke_wins=False):
        if naruto_wins:
            if self.right:
                win.blit(walkRight[2], (self.x, self.y))
            else:
                win.blit(walkLeft[2], (self.x, self.y))
            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        elif self.health > 0 and not sasuke_wins:
            if self.walkCount + 1 >= 6:
                self.walkCount = 0
            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//2], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//2], (self.x, self.y))
                    self.walkCount +=1
            else:
                if self.right:
                    win.blit(walkRight[2], (self.x, self.y))
                else:
                    win.blit(walkLeft[2], (self.x, self.y))
            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
            pygame.draw.rect(win, (255, 0, 0), (80, 40, 210, 25))
            health_width = int(210 * (self.health / self.max_health))
            pygame.draw.rect(win, (255, 255, 0), (80, 45, health_width, 15))
        else:
            win.blit(naruto_dead, (self.x, self.y))
    def hit(self):
        if self.health > 0:
            self.health -= 5
            if hitSound and sound_enabled:
                hitSound.play()

class enemy:
    walkRightS = [load_image('SR2.png'), load_image('SR3.png'), load_image('SR1.png')]
    walkLeftS = [load_image('SL2.png'), load_image('SL3.png'), load_image('SL1.png')]
    def __init__(self, x, y, width, height, end, speed=8):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [10, end]
        self.speed = speed
        self.original_speed = speed
        self.walkCount = 0
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        self.health = 200
        self.max_health = 200
        self.isjump = False
        self.jumpheight = 10
        self.last_shuriken_time = 0
        self.shuriken_cooldown = 0
        self.last_jump_time = 0
        self.jump_cooldown = 0
    def draw(self, win, naruto_wins=False, sasuke_wins=False):
        self.move()
        if sasuke_wins:
            if self.speed >= 0:
                win.blit(self.walkRightS[2], (self.x, self.y))
            else:
                win.blit(self.walkLeftS[2], (self.x, self.y))
            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        elif self.health > 0:
            if self.walkCount + 1 >= 6:
                self.walkCount = 0
            if self.speed > 0:
                win.blit(self.walkRightS[self.walkCount//2], (self.x, self.y))
                self.walkCount +=1
            else:
                win.blit(self.walkLeftS[self.walkCount//2], (self.x, self.y))
                self.walkCount +=1
            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
            pygame.draw.rect(win, (255, 0, 0), (410, 40, 210, 25))
            health_width = int(210 * (self.health / self.max_health))
            pygame.draw.rect(win, (255, 255, 0), (410 + (210 - health_width), 45, health_width, 15))
        else:
            self.speed = 0
            win.blit(sasuke_dead, (self.x, self.y))
    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0
        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0
    def jump(self):
        if not self.isjump:
            self.isjump = True
            self.jumpheight = 10
    def update_jump(self):
        if self.isjump:
            if self.jumpheight >= -10:
                neg = -1 if self.jumpheight < 0 else 1
                self.y -= (self.jumpheight ** 2) * 0.5 * neg
                self.jumpheight -= 1
            else:
                self.isjump = False
                self.jumpheight = 10
    def hit(self):
        if self.health > 0:
            self.health -= 10
            if hitSound and sound_enabled:
                hitSound.play()

class weapons:
    def __init__(self, x, y, width, height, facing):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.facing = facing
        self.vel = 8 * facing
        self.hitbox = (self.x, self.y, 100, 40)
    def draw(self, win):
        win.blit(shuriken_img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 40, 40)

def show_text(text, size=60, duration=2):
    font = font_medium if size == 60 else font_large if size == 80 else font_small
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(350, 250))
    overlay = pygame.Surface((700, 500), pygame.SRCALPHA)
    overlay.fill((0, 0, 20, 128))
    win.blit(overlay, (0, 0))
    win.blit(text_surface, text_rect)
    pygame.display.update()
    time.sleep(duration)

def draw_start_screen():
    global start_gif
    frame = start_gif.get_current_frame()
    bg_rect = frame.get_rect(center=(350, 250))
    win.blit(frame, bg_rect)
    title = font_medium.render("Naruto vs Sasuke", True, (255, 255, 255))
    button = font_small.render("START", True, (150, 10, 205))
    button_rect = pygame.Rect(250, 300, 200, 70)
    pygame.draw.rect(win, (255, 255, 255), button_rect)
    win.blit(title, (100, 100))
    win.blit(button, (button_rect.x + 45, button_rect.y + 10))
    pygame.display.update()
    return button_rect

level_bg = load_image(random.choice(backgrounds))
last_bg_change = time.time()

def draw_level_screen(highest_level, mouse_pos):
    global level_bg, last_bg_change
    current_time = time.time()
    if current_time - last_bg_change >= 2.5:
        level_bg = load_image(random.choice(backgrounds))
        last_bg_change = current_time
    bg_rect = level_bg.get_rect(center=(350, 250))
    win.blit(level_bg, bg_rect)
    overlay = pygame.Surface((700, 500), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    win.blit(overlay, (0, 0))
    title = font_medium.render("Select Level", True, (255, 255, 255))
    title_shadow = font_medium.render("Select Level", True, (0, 0, 0))
    win.blit(title_shadow, (182, 52))
    win.blit(title, (180, 50))
    level_buttons = []
    max_levels = 8
    start_x = 110
    start_y = 150
    button_size = 80
    spacing_x = 140
    spacing_y = 100
    for i in range(1, max_levels + 1):
        col = (i - 1) % 4
        row = (i - 1) // 4
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        button_rect = pygame.Rect(x, y, button_size, button_size)
        is_playable = i <= highest_level
        button_color = (255, 165, 0) if is_playable else (50, 50, 50)
        pygame.draw.rect(win, button_color, button_rect, border_radius=10)
        text = font_small.render(str(i), True, (255, 255, 255) if is_playable else (100, 100, 100))
        text_rect = text.get_rect(center=button_rect.center)
        win.blit(text, text_rect)
        if is_playable and button_rect.collidepoint(mouse_pos):
            glow_size = 4 + 2 * math.sin(time.time() * 5)
            glow_rect = button_rect.inflate(glow_size * 2, glow_size * 2)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 255, 0, 100), glow_surface.get_rect(), border_radius=12, width=int(glow_size))
            win.blit(glow_surface, glow_rect)
        level_buttons.append((button_rect, i))
    restart_text = font_small.render("Restart Game", True, (255, 255, 255))
    restart_rect = pygame.Rect(225, 400, 250, 50)
    pygame.draw.rect(win, (255, 165, 0), restart_rect, border_radius=10)
    restart_text_rect = restart_text.get_rect(center=restart_rect.center)
    win.blit(restart_text, restart_text_rect)
    if restart_rect.collidepoint(mouse_pos):
        glow_size = 4 + 2 * math.sin(time.time() * 5)
        glow_rect = restart_rect.inflate(glow_size * 2, glow_size * 2)
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (255, 255, 0, 100), glow_surface.get_rect(), border_radius=12, width=int(glow_size))
        win.blit(glow_surface, glow_rect)
    pygame.display.update()
    return level_buttons, restart_rect

def redrawgamewindow(level, sasuke_shurikens, health_potions, paused=False, naruto_wins=False, sasuke_wins=False, naruto_health=200, sasuke_health=200):
    win.blit(bg, (0, 0))
    if level > 2:
        for potion in health_potions:
            potion.draw(win)
    naruto.draw(win, naruto_wins=naruto_wins, sasuke_wins=sasuke_wins)
    sasuke.draw(win, naruto_wins=naruto_wins, sasuke_wins=sasuke_wins)
    win.blit(Nh, (10, 10))
    win.blit(Sh, (600, 10))
    level_text = font_level.render(f"Level {level}", True, (255, 255, 255))
    win.blit(level_text, (350 - level_text.get_width()//2, 45))
    pause_rect = pygame.Rect(325, 10, 40, 40)
    if not (naruto_wins or sasuke_wins):
        pygame.draw.rect(win, (255, 165, 0), pause_rect, border_radius=10)
        pause_text = font_pause.render("P", True, (255, 255, 255))
        pause_text_rect = pause_text.get_rect(center=pause_rect.center)
        win.blit(pause_text, pause_text_rect)
    if level > 2:
        potion_count = sum(1 for p in health_potions if not p.collected)
        
    for shuriken in shurikens:
        shuriken.draw(win)
    for shuriken in sasuke_shurikens:
        shuriken.draw(win)
    if naruto_wins:
        overlay = pygame.Surface((700, 500), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        win.blit(overlay, (0, 0))
        scale = 0.9 + 0.2 * (math.sin(time.time() * 3) / 2 + 0.5)
        main_text = font_large.render("Naruto Wins!", True, (255, 255, 0))
        main_shadow = font_large.render("Naruto Wins!", True, (0, 0, 0))
        main_rect = main_text.get_rect(center=(350, 250))
        shadow_rect = main_shadow.get_rect(center=(353, 253))
        scaled_text = pygame.transform.scale(main_text, (int(main_rect.width * scale), int(main_rect.height * scale)))
        scaled_shadow = pygame.transform.scale(main_shadow, (int(shadow_rect.width * scale), int(shadow_rect.height * scale)))
        scaled_rect = scaled_text.get_rect(center=(350, 250))
        scaled_shadow_rect = scaled_shadow.get_rect(center=(353, 253))
        win.blit(scaled_shadow, scaled_shadow_rect)
        win.blit(scaled_text, scaled_rect)
        level_text = font_small.render(f"Level {level} Completed", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(350, 320))
        win.blit(level_text, level_rect)
        health_text = font_very_small.render(f"Naruto: {naruto_health}/200 | Sasuke: 0/200", True, (255, 255, 255))
        health_rect = health_text.get_rect(center=(350, 360))
        win.blit(health_text, health_rect)
    if sasuke_wins:
        overlay = pygame.Surface((700, 500), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        win.blit(overlay, (0, 0))
        scale = 0.9 + 0.2 * (math.sin(time.time() * 3) / 2 + 0.5)
        main_text = font_large.render("Sasuke Wins!", True, (255, 0, 0))
        main_shadow = font_large.render("Sasuke Wins!", True, (0, 0, 0))
        main_rect = main_text.get_rect(center=(350, 250))
        shadow_rect = main_shadow.get_rect(center=(353, 253))
        scaled_text = pygame.transform.scale(main_text, (int(main_rect.width * scale), int(main_rect.height * scale)))
        scaled_shadow = pygame.transform.scale(main_shadow, (int(shadow_rect.width * scale), int(shadow_rect.height * scale)))
        scaled_rect = scaled_text.get_rect(center=(350, 250))
        scaled_shadow_rect = scaled_shadow.get_rect(center=(353, 253))
        win.blit(scaled_shadow, scaled_shadow_rect)
        win.blit(scaled_text, scaled_rect)
        level_text = font_small.render(f"Level {level} Failed", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(350, 320))
        win.blit(level_text, level_rect)
        health_text = font_very_small.render(f"Naruto: 0/200 | Sasuke: {sasuke_health}/200", True, (255, 255, 255))
        health_rect = health_text.get_rect(center=(350, 360))
        win.blit(health_text, health_rect)
        retry_rect = pygame.Rect(225, 400, 250, 50)
        pygame.draw.rect(win, (255, 165, 0), retry_rect, border_radius=10)
        retry_text = font_small.render("Retry Level", True, (255, 255, 255))
        retry_text_rect = retry_text.get_rect(center=retry_rect.center)
        win.blit(retry_text, retry_text_rect)
        return_rect = pygame.Rect(225, 460, 250, 50)
        pygame.draw.rect(win, (255, 165, 0), return_rect, border_radius=10)
        return_text = font_small.render("Return to Start", True, (255, 255, 255))
        return_text_rect = return_text.get_rect(center=return_rect.center)
        win.blit(return_text, return_text_rect)
    if paused:
        overlay = pygame.Surface((700, 500), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        win.blit(overlay, (0, 0))
        continue_rect = pygame.Rect(225, 200, 250, 50)
        pygame.draw.rect(win, (255, 165, 0), continue_rect, border_radius=10)
        continue_text = font_small.render("Continue", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=continue_rect.center)
        win.blit(continue_text, continue_text_rect)
        retry_rect = pygame.Rect(225, 250, 250, 50)
        pygame.draw.rect(win, (255, 165, 0), retry_rect, border_radius=10)
        retry_text = font_small.render("Retry Level", True, (255, 255, 255))
        retry_text_rect = retry_text.get_rect(center=retry_rect.center)
        win.blit(retry_text, retry_text_rect)
        exit_rect = pygame.Rect(225, 300, 250, 50)
        pygame.draw.rect(win, (255, 165, 0), exit_rect, border_radius=10)
        exit_text = font_small.render("Exit", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=exit_rect.center)
        win.blit(exit_text, exit_text_rect)
        sound_rect = pygame.Rect(225, 350, 250, 50)
        pygame.draw.rect(win, (255, 165, 0), sound_rect, border_radius=10)
        sound_text = font_small.render(f"Sound: {'On' if sound_enabled else 'Off'}", True, (255, 255, 255))
        sound_text_rect = sound_text.get_rect(center=sound_rect.center)
        win.blit(sound_text, sound_text_rect)
    pygame.display.update()
    return (pause_rect, continue_rect if paused else None, retry_rect if paused else None, 
            exit_rect if paused else None, sound_rect if paused else None, 
            retry_rect if sasuke_wins else None, return_rect if sasuke_wins else None)

def reset_game(level):
    global naruto, sasuke, shurikens, throwSpeed, run, bg, current_bg, health_potions
    available_bgs = [b for b in backgrounds if b != current_bg]
    current_bg = random.choice(available_bgs) if available_bgs else random.choice(backgrounds)
    bg = load_image(current_bg)
    naruto = player(30, 400, 100, 100)
    sasuke_speed = 8 + 3 * (level - 1)
    sasuke = enemy(100, 400, 100, 100, 600, sasuke_speed)
    shurikens = []
    throwSpeed = 0
    run = True
    health_potions = []
    if level > 2:
        for _ in range(random.randint(2, 3)):
            x = random.randint(100, 600)
            y = random.randint(250, 450)
            health_potions.append(HealthPotion(x, y))
    show_text(f"Level {level}", 80, 1.5)

highest_level = load_progress()
start_gif = GifAnimation('front 2.jpg', frame_count=1, frame_duration=0.5)

start_button = draw_start_screen()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                waiting = False
    draw_start_screen()
    Clock.tick(30)

level_buttons, restart_button = draw_level_screen(highest_level, pygame.mouse.get_pos())
selecting_level = True
selected_level = None
while selecting_level:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_rect, lvl in level_buttons:
                if button_rect.collidepoint(event.pos) and lvl <= highest_level:
                    selected_level = lvl
                    selecting_level = False
            if restart_button.collidepoint(event.pos):
                highest_level = 1
                save_progress(highest_level)
                selected_level = 1
                selecting_level = False
    level_buttons, restart_button = draw_level_screen(highest_level, mouse_pos)
    Clock.tick(60)

level = selected_level if selected_level else 1
shurikens = []
sasuke_shurikens = []
health_potions = []
throwSpeed = 0
reset_game(level)
running = True
paused = False
while running:
    while run:
        Clock.tick(25)
        current_time = time.time()
        naruto_wins = sasuke.health <= 0
        sasuke_wins = naruto.health <= 0
        pause_rect, continue_rect, retry_rect_pause, exit_rect, sound_rect, retry_rect_go, return_rect = redrawgamewindow(
            level, sasuke_shurikens, health_potions, paused, naruto_wins, sasuke_wins, 
            naruto_health=int(naruto.health), sasuke_health=int(sasuke.health))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos) and not paused and not (naruto_wins or sasuke_wins):
                    paused = True
                    sasuke.speed = 0
                if paused:
                    if continue_rect and continue_rect.collidepoint(event.pos):
                        paused = False
                        sasuke.speed = sasuke.original_speed
                    if retry_rect_pause and retry_rect_pause.collidepoint(event.pos):
                        reset_game(level)
                        paused = False
                        sasuke.speed = sasuke.original_speed
                    if exit_rect and exit_rect.collidepoint(event.pos):
                        run = False
                    if sound_rect and sound_rect.collidepoint(event.pos):
                        sound_enabled = not sound_enabled
                        if sound_enabled:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                if sasuke_wins:
                    if retry_rect_go and retry_rect_go.collidepoint(event.pos):
                        sasuke_shurikens = []
                        reset_game(level)
                        paused = False
                    if return_rect and return_rect.collidepoint(event.pos):
                        run = False
            if event.type == pygame.KEYDOWN and not (naruto_wins or sasuke_wins):
                if event.key == pygame.K_p and not paused:
                    paused = True
                    sasuke.speed = 0
                elif event.key == pygame.K_p and paused:
                    paused = False
                    sasuke.speed = sasuke.original_speed
        if paused or naruto_wins or sasuke_wins:
            if naruto_wins:
                time.sleep(3)
                level += 1
                if level > highest_level:
                    highest_level = level
                    save_progress(highest_level)
                sasuke_shurikens = []
                reset_game(level)
            continue
        if throwSpeed > 0:
            throwSpeed += 1
        if throwSpeed > 3:
            throwSpeed = 0
        if level > 2:
            if current_time - sasuke.last_shuriken_time > sasuke.shuriken_cooldown:
                sasuke.last_shuriken_time = current_time
                sasuke.shuriken_cooldown = random.uniform(1, 5)
                facing = -1 if sasuke.speed < 0 else 1
                num_shurikens = random.randint(1, 5)
                for _ in range(num_shurikens):
                    y_offset = random.randint(-20, 20)
                    sasuke_shurikens.append(weapons(round(sasuke.x + 60), round(sasuke.y + 30 + y_offset), 40, 40, facing))
            if current_time - sasuke.last_jump_time > sasuke.jump_cooldown:
                sasuke.last_jump_time = current_time
                sasuke.jump_cooldown = random.uniform(2, 8)
                sasuke.jump()
        sasuke.update_jump()
        if level > 2 and naruto.isjump:
            for potion in health_potions[:]:
                if not potion.collected:
                    if (naruto.hitbox[0] < potion.hitbox[0] + potion.hitbox[2] and naruto.hitbox[0] + naruto.hitbox[2] > potion.hitbox[0] and naruto.hitbox[1] < potion.hitbox[1] + potion.hitbox[3] and naruto.hitbox[1] + naruto.hitbox[3] > potion.hitbox[1]):
                        potion.collected = True
                        naruto.health = min(naruto.health + 20, naruto.max_health)
                        if hitSound and sound_enabled:
                            hitSound.play()
        if naruto.health > 0 and sasuke.health > 0:
            if (naruto.hitbox[1] < sasuke.hitbox[1] + sasuke.hitbox[3] and naruto.hitbox[1] + naruto.hitbox[3] > sasuke.hitbox[1] and naruto.hitbox[0] + naruto.hitbox[2] > sasuke.hitbox[0] and naruto.hitbox[0] < sasuke.hitbox[0] + sasuke.hitbox[2]):
                naruto.hit()
        for shuriken in shurikens[:]:
            if sasuke.health > 0:
                if (shuriken.hitbox[1] + shuriken.hitbox[3]//2 > sasuke.hitbox[1] and shuriken.hitbox[1] + shuriken.hitbox[3]//2 < sasuke.hitbox[1] + sasuke.hitbox[3] and shuriken.hitbox[0] + shuriken.hitbox[2] > sasuke.hitbox[0] and shuriken.hitbox[0] < sasuke.hitbox[0] + sasuke.hitbox[2]):
                    sasuke.hit()
                    shurikens.remove(shuriken)
            if 0 < shuriken.x < 700:
                shuriken.x += shuriken.vel
            else:
                shurikens.remove(shuriken)
        for shuriken in sasuke_shurikens[:]:
            if naruto.health > 0:
                if (shuriken.hitbox[1] + shuriken.hitbox[3]//2 > naruto.hitbox[1] and shuriken.hitbox[1] + shuriken.hitbox[3]//2 < naruto.hitbox[1] + naruto.hitbox[3] and shuriken.hitbox[0] + shuriken.hitbox[2] > naruto.hitbox[0] and shuriken.hitbox[0] < naruto.hitbox[0] + naruto.hitbox[2]):
                    naruto.hit()
                    sasuke_shurikens.remove(shuriken)
            if 0 < shuriken.x < 700:
                shuriken.x += shuriken.vel
            else:
                sasuke_shurikens.remove(shuriken)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and throwSpeed == 0:
            facing = -1 if naruto.left else 1
            if len(shurikens) < 5:
                shurikens.append(weapons(round(naruto.x + 60), round(naruto.y + 30), 40, 40, facing))
            throwSpeed = 1
        if keys[pygame.K_LEFT] and naruto.x > naruto.speed:
            naruto.x -= naruto.speed
            naruto.left = True
            naruto.right = False
            naruto.standing = False
        elif keys[pygame.K_RIGHT] and naruto.x < 700 - naruto.width - naruto.speed:
            naruto.x += naruto.speed
            naruto.left = False
            naruto.right = True
            naruto.standing = False
        else:
            naruto.standing = True
            naruto.walkCount = 0
        if not naruto.isjump:
            if keys[pygame.K_UP]:
                naruto.isjump = True
                naruto.left = False
                naruto.right = False
                naruto.walkCount = 0
        else:
            if naruto.jumpheight >= -10:
                neg = -1 if naruto.jumpheight < 0 else 1
                naruto.y -= (naruto.jumpheight ** 2) * 0.5 * neg
                naruto.jumpheight -= 1
            else:
                naruto.isjump = False
                naruto.jumpheight = 10
    if not run:
        start_button = draw_start_screen()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        waiting = False
                        level_buttons, restart_button = draw_level_screen(highest_level, pygame.mouse.get_pos())
                        selecting_level = True
                        while selecting_level:
                            mouse_pos = pygame.mouse.get_pos()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    for button_rect, lvl in level_buttons:
                                        if button_rect.collidepoint(event.pos) and lvl <= highest_level:
                                            level = lvl
                                            selecting_level = False
                                    if restart_button.collidepoint(event.pos):
                                        highest_level = 1
                                        save_progress(highest_level)
                                        level = 1
                                        selecting_level = False
                            level_buttons, restart_button = draw_level_screen(highest_level, mouse_pos)
                            Clock.tick(60)
                        sasuke_shurikens = []
                        reset_game(level)
                        run = True
                        paused = False
            draw_start_screen()
            Clock.tick(30)
pygame.quit()
sys.exit()