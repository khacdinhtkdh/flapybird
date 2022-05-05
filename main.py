import pygame, sys, random

score = 0
high_score = 0


def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pip_height)
    bottom_pipe = pip_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pip_surface.get_rect(midtop=(500, random_pipe_pos - 700))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pip_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pip_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False

    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 620))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()

# background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)

# bird
bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_mid = pygame.transform.scale2x(bird_mid)
bird_down = pygame.transform.scale2x(bird_down)
bird_up = pygame.transform.scale2x(bird_up)
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

# bird timer
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

# pipe
pip_surface = pygame.image.load('assets/pipe-green.png').convert()
pip_surface = pygame.transform.scale2x(pip_surface)

# timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 3000)

# score
game_font = pygame.font.Font('04B_19.ttf', 40)

pip_height = [250, 300, 350, 400]
floor_x_pos = 0
gravity = 0.2
bird_movement = 0
pip_list = []
game_active = True

# end game
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                score = 0
                pip_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
        if event.type == spawn_pipe:
            pip_list.extend(create_pipe())
        if event.type == bird_flap:
            bird_index = (bird_index + 1) % 3
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pip_list)

        pip_list = move_pipe(pip_list)
        draw_pipe(pip_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound_countdown = 100
            score_sound.play()
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game over')

    floor_x_pos -= 1
    if floor_x_pos <= -432:
        floor_x_pos = 0
    draw_floor()
    pygame.display.update()
    clock.tick(120)
