import math
import random
import os

from pygame import Rect

os.environ['SDL_VIDEO_CENTERED'] = '1'

FULLSCREEN = False
WIDTH = 1280
HEIGHT = 720

def spawn_enemy_sprite(enemy_dict):
    side = random.randint(1,4)
    sprite = enemy_dict["sprite"]

    if side == 1:  # Cima
        sprite.x = random.randint(0, WIDTH)
        sprite.y = -50
    elif side == 2:  # Baixo
        sprite.x = random.randint(0, WIDTH)
        sprite.y = HEIGHT + 50
    elif side == 3:  # Esquerda
        sprite.x = -50
        sprite.y = random.randint(0, HEIGHT)
    else:  # Direita
        sprite.x = WIDTH + 50
        sprite.y = random.randint(0, HEIGHT)

TITLE = "Aventura de Jhon"

game_state = "MENU"
message = "Acabe com a invasão dos esqueletos"


start_message = "Uma nova aventura inicia"
game_over_menssage = "Tente novamente"
message_fire = ""


player = Actor('walk_front_left', (100,100))
player_anim_counter = 0
player_frame = 1
player_action_timer = 0

enemy = Rect((600, 400), (50,50))

enemies = []
for i in range(10):
    en_actor = Actor('enemy_run_front_left')
    en = {
        "sprite": en_actor,
        "speed": random.randint(1, 3),
        "frame":1,
        "anim_counter": 0
    }
    spawn_enemy_sprite(en)
    enemies.append(en)

speed = 5

bullets = []
bullet_speed = 10

mouse_pos = (WIDTH // 2, HEIGHT // 2)

# Posições dos botões no Menu
btn_start = Rect((WIDTH//2 - 100, HEIGHT//2 - 50), (200, 50))
btn_music = Rect((WIDTH//2 - 100, HEIGHT//2 + 20), (200, 50))
btn_exit  = Rect((WIDTH//2 - 100, HEIGHT//2 + 90), (200, 50))
bnt_back_menu = Rect((WIDTH//2 - 100, HEIGHT//2 + 160), (200, 50))

music_on = True # Variável para controlar o estado da música

def reset_message():
    global message_fire
    message_fire = ""

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

def on_mouse_down(pos, button):
    global message_fire, start_message, game_state,music_on

    if game_state == "MENU":
        if button == mouse.LEFT:
            #Clicar no botão de iniciar
            if btn_start.collidepoint(pos):
                game_state = "PLAYING"
                for en in enemies:
                    spawn_enemy_sprite(en)
                return
            # Clicar no botão de musica
            if btn_music.collidepoint(pos):
                music_on = not music_on
                if music_on:
                    music.play("music_game")
                else:
                    music.stop()
            # Clicar no botão de Sair
            if btn_exit.collidepoint(pos):
                os._exit(0)
    # Clicar no botão para voltar ao menu
    if game_state == "GAME OVER":
        if button == mouse.LEFT:
            # Clicar no botão de iniciar
            if bnt_back_menu.collidepoint(pos):
                game_state = "MENU"
                player.topleft = (100,100)
                bullets.clear()
                if music_on:
                    music.play("music_game")
            return

    if button == mouse.LEFT and game_state == 'PLAYING':
        message_fire = "Voce disparou!"
        if music_on:
            sounds.arrow.play()
        clock.unschedule(reset_message)
        clock.schedule(reset_message, 1.0)

        dx = pos[0] - player.centerx
        dy = pos[1] - player.centery

        distancy = math.hypot(dx ,dy)

        if distancy > 0 :
            vx = (dx / distancy) * 10 # 10 é a velocidade da bala
            vy = (dy / distancy) * 10

            newBullet = {
            "rect": Rect((player.centerx, player.centery), (8, 8)),
            "vx": vx,
            "vy": vy,
            }
            bullets.append(newBullet)

    if button == mouse.LEFT and game_state == 'PLAYING':
        player.image = 'watering_armon'
        player_action_timer = 20

def draw():
    screen.clear()
    screen.fill((30, 100, 40))

    if game_state == "MENU":
        screen.blit('menu_screen', (0, 0))
        screen.draw.text("AVENTURA DE JHON", center=(WIDTH//2, HEIGHT//2 - 160), fontsize=70, color="white")
        screen.draw.text("Clique com o mouse para inciar", center=(WIDTH//2, HEIGHT//2 -100), fontsize=60, color=(139,69,19))
        screen.draw.text("User as teclas WASD ou as setas direcionais do teclado para se mover e o mouse para atirar", center=(WIDTH//2, HEIGHT//2 + 200), fontsize=35, color="white")

        screen.draw.filled_rect(btn_start, "green")
        screen.draw.text("INICIAR", center=btn_start.center, fontsize=30, color="white")

        color_music = "blue" if music_on else "gray"
        screen.draw.filled_rect(btn_music, color_music)
        txt_music = "MUSICA: LIGADA" if music_on else "MUSICA: DESLIGADA"
        screen.draw.text(txt_music, center=btn_music.center, fontsize=20, color="white")

        # Botão Sair
        screen.draw.filled_rect(btn_exit, "red")
        screen.draw.text("SAIR", center=btn_exit.center, fontsize=30, color="white")

    elif game_state == "PLAYING" or game_state == "GAME OVER":
        screen.blit('mapa', (0, 0))

        screen.draw.text(start_message, (50, 50), fontsize=50)
        screen.draw.text(message_fire, (550, 50), fontsize=50)
        player.draw() # O Actor desenha a imagem automaticamente na posição x, y

        for enemy in enemies:
            enemy["sprite"].draw()  # O Actor já sabe se desenhar

        screen.draw.text(message, (20,20), fontsize=30, color="white")

        if game_state == 'GAME OVER':
            screen.blit('defeat_screen', (0, 0))
            screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="red")
            screen.draw.text("Pressione R para reiniciar a fase", center=(WIDTH // 2, HEIGHT // 2 + 40), fontsize=30, color="white")

            # Botão Voltar
            screen.draw.filled_rect(bnt_back_menu, "blue")
            # USE bnt_back_menu.center AQUI:
            screen.draw.text("MENU PRINCIPAL", center=bnt_back_menu.center, fontsize=20, color="white")

        for b in bullets:
            screen.draw.filled_rect(b["rect"], "yellow")


    mx, my = mouse_pos
    screen.draw.circle((mx, my), 15, "black")
    screen.draw.line((mx - 10, my), (mx + 10, my), "red")
    screen.draw.line((mx, my - 10), (mx, my + 10), "red")

def on_key_down(key): # Criando uma atualização para a tela, quando o botão do espaço for curado então vai aparecer o Voce apertou espaco
    global message_fire, game_state, player, start_message

    if key == keys.R and game_state == 'GAME OVER':
        # Resetar o jogo
        player.topleft = (100, 100)
        game_state = 'PLAYING'
        start_message = "Uma nova aventura inicia"
        if music_on:
            music.play("music_game")

        #Manda os inimigos para as bordas quando o jogo reinicia
        for en in enemies:
                spawn_enemy_sprite(en)
        #Limpa as balas da tela
        bullets.clear()

def update():
    global start_message, message_fire, message, game_state

    if game_state == "PLAYING":
        update_player()
        update_enemies()
        update_bullet()

def update_player():
    global player_anim_counter, player_framem, player_action_timer, player_frame

    # 1. Diminuir o timer de ação
    if player_action_timer > 0:
        player_action_timer -= 1
        player.image = 'watering_armon'  # Garante que a imagem fique fixa enquanto atira

    moving = False
# Movimento
    if keyboard.a or keyboard.left:
        player.x -= speed
        moving = True
    if keyboard.d or keyboard.right:
        player.x += speed
        moving = True
    if keyboard.w or keyboard.up:
        player.y -= speed
        moving = True
    if keyboard.s or keyboard.down:
        player.y += speed
        moving = True

        # 3. Lógica de Animação (Só roda se NÃO estiver atirando)
        if player_action_timer <= 0:
            if moving:
                player_anim_counter += 1
                if player_anim_counter > 10:
                    player_anim_counter = 0
                    if player_frame == 1:
                        player_frame = 2
                        player.image = 'walk_front_right'
                    else:
                        player_frame = 1
                        player.image = 'walk_front_left'
            else:
                player.image = 'walk_front_left'

    # Limites da tela usando as propriedades do Actor
    player.x = max(25, min(player.x, WIDTH - 25))
    player.y = max(25, min(player.y, HEIGHT - 25))

#Colisão
def update_enemies():
    global game_state, start_message
    for enemy in enemies:
        s = enemy["sprite"]
        speed_enemy = enemy["speed"]

        # Movendo o sprite em direção ao player
        if s.x < player.x: s.x += speed_enemy
        if s.x > player.x: s.x -= speed_enemy
        if s.y < player.y: s.y += speed_enemy
        if s.y > player.y: s.y -= speed_enemy

        enemy["anim_counter"] += 1

        if enemy["anim_counter"] > 10: # Troca de animação altara caso queira que fique mais rapido
            enemy["anim_counter"] = 0

            if enemy["frame"] == 1:
                enemy["frame"] = 2
                s.image = 'enemy_run_front_right'
            else:
                enemy["frame"] = 1
                s.image = 'enemy_run_front_left'

        # Colisão usando o método .colliderect do Actor
        if s.colliderect(player):
            if game_state != "GAME OVER":
                game_state = "GAME OVER"
                bullets.clear()
                if music_on:
                    music.play("defeat")

def update_bullet():
    for b in bullets[:]:
        b["rect"].x += b["vx"]
        b["rect"].y += b["vy"]
        if b["rect"].x < 0 or b["rect"].x > WIDTH or b["rect"].y < 0 or b["rect"].y > HEIGHT:
            bullets.remove(b)
            continue

        for en in enemies:
            if en["sprite"].colliderect(b["rect"]):
                spawn_enemy_sprite(en)
                if music_on:
                    sounds.bone_break_sound.play()
                if b in bullets:
                    bullets.remove(b)
                break

import pgzrun
music.play("music_game")
music.set_volume(0.1)
pgzrun.go()