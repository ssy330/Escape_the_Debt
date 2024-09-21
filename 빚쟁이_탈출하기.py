import pygame
import sys
import random
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from 미니게임_py import cup_game
from 미니게임_py import horse_game
from 미니게임_py import arbeit
from 미니게임_py import lotto

root = tk.Tk()
root.withdraw()

def end_game():
    game_duration = datetime.now() - start_time
    minutes, seconds = divmod(game_duration.seconds, 60)
    messagebox.showinfo("게임 종료", f"빛 청산까지 {minutes}분 {seconds}초 걸렸습니다.")
    initialize_game()

def initialize_game():
    global score, last_item_time, thief_active, thief_timer, out, last_time, start_time
    score = -50000
    last_item_time = pygame.time.get_ticks()
    thief_active = False
    thief_timer = pygame.time.get_ticks()
    out = False
    last_time = pygame.time.get_ticks()
    start_time = datetime.now()

initialize_game()
    
# 초기화
pygame.init()

# 메인 화면 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("메인 화면")

# 메뉴 아이콘
menu_icon_img = pygame.image.load("이미지/메뉴아이콘.png")  
menu_icon_img = pygame.transform.scale(menu_icon_img, (50, 50)) 
menu_icon_rect = menu_icon_img.get_rect(topleft=(10, 10))

# 메뉴 화면 설정
menu_rect = pygame.Rect(200, 150, 400, 300)
menu_active = False
    
# 뒤로가기 설정
back_icon_img = pygame.image.load("이미지/뒤로가기.png")  
back_icon_img = pygame.transform.scale(back_icon_img, (50, 50)) 
back_icon_rect = back_icon_img.get_rect(topleft=(10, 10))

# 버튼 설정
menu_button1_img = pygame.image.load("이미지/버튼1.png")
menu_button1_img = pygame.transform.scale(menu_button1_img, (160, 120)) 
menu_button1_rect = pygame.Rect(225, 210, 160, 120)

menu_button2_img = pygame.image.load("이미지/버튼2.png")
menu_button2_img = pygame.transform.scale(menu_button2_img, (160, 120)) 
menu_button2_rect = pygame.Rect(420, 210, 160, 120)

menu_button3_img = pygame.image.load("이미지/버튼3.png")
menu_button3_img = pygame.transform.scale(menu_button3_img, (160, 120)) 
menu_button3_rect = pygame.Rect(225, 300, 160, 120)

menu_button4_img = pygame.image.load("이미지/버튼4.png")
menu_button4_img = pygame.transform.scale(menu_button4_img, (160, 120)) 
menu_button4_rect = pygame.Rect(420, 300, 160, 120)


# 이미지 로드 / 크기 조절
background_image = pygame.image.load("이미지/메인 배경.png")
background_image = pygame.transform.scale(background_image, (width, height))

character_img = pygame.image.load("이미지/캐릭터.png")
item1_img = pygame.image.load("이미지/소주병.png")
item2_img = pygame.image.load("이미지/폐지.png")
thief_img = pygame.image.load("이미지/도둑.png")

character_width, character_height = 70, 100
character_img = pygame.transform.scale(character_img, (character_width, character_height))

item_width, item_height = 50, 50
item_width1, item_height1 = 20, 50
item_width2, item_height2 = 40, 50
item1_img = pygame.transform.scale(item1_img, (item_width1, item_height1))
item2_img = pygame.transform.scale(item2_img, (item_width2, item_height2))

thief_width, thief_height = 70, 100
thief_img = pygame.transform.scale(thief_img, (thief_width, thief_height))


# 캐릭터 초기 설정
character_rect = character_img.get_rect()
character_rect.center = (width//2, 600//2)


# 아이템 초기 설정 (소주병, 폐지)
max_items = 7  # 최대 아이템 생성 갯수
items = []  
for _ in range(max_items):  
    item_type = random.choice([1, 2])
    if item_type == 1:
        item_img = item1_img
    else:
        item_img = item2_img

    item_rect = pygame.Rect(random.randint(50, width - 50 - item_width), random.randint(200, height - 50 - item_height), item_width1, item_height1)
    items.append((item_type, item_rect)) 

# 도둑 초기 설정 (초기 위치는 왼쪽 아래)
thief_rect = pygame.Rect(-thief_width, height - thief_height, thief_width, thief_height)
thief_active = False
thief_timer = pygame.time.get_ticks() 

# 점수 및 시간 초기화
score = -50000
last_item_time = pygame.time.get_ticks()

# 이동 관련 변수 설정
speed = 5  # 이동 속도
target_pos = (0, 0)  # 목표 위치

        
# 게임 루프
clock = pygame.time.Clock()

running = True
out = False
last_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            target_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if menu_icon_rect.collidepoint(event.pos):
                menu_active = not menu_active
            elif menu_active == True and menu_button1_rect.collidepoint(event.pos):
                score = cup_game.Cup_game(score)
            elif menu_active == True and menu_button2_rect.collidepoint(event.pos):
                score = horse_game.Horse_game(score)           
            elif menu_active == True and menu_button3_rect.collidepoint(event.pos):
                score = arbeit.Arbeit(score)  
            elif menu_active == True and menu_button4_rect.collidepoint(event.pos):
                score = lotto.Lotto(score)
                

    # 마우스를 움직이면 캐릭터가 따라옴
    dx = target_pos[0] - character_rect.centerx
    dy = target_pos[1] - character_rect.centery
  
    distance = pygame.math.Vector2(dx, dy).length()

    if distance != 0:
        character_rect.x += dx * speed / distance
        character_rect.y += dy * speed / distance

    # 아이템과 캐릭터 충돌 검사
    for item_type, item_rect in items:
        if character_rect.colliderect(item_rect):
            score += 100
            items.remove((item_type, item_rect))

    # 시간이 1초 경과하면 아이템 생성
    current_time = pygame.time.get_ticks()
    if current_time - last_item_time >= 1000: 
        if len(items) < max_items:
            new_item_rect = pygame.Rect(random.randint(50, width - 50 - item_width), random.randint(200, height - 50 - item_height), item_width, item_height)
            items.append((random.choice([1, 2]), new_item_rect))
            last_item_time = current_time


    # 도둑의 활성화 여부 확인
    if not thief_active:
        # 도둑이 나타나기까지의 시간 체크
        current_time = pygame.time.get_ticks()
        if current_time - last_time >= random.randint(10000, 20000):  
            thief_active = True
            thief_rect.x = -thief_width
            thief_rect.y = height - thief_height 
            thief_timer = current_time
            

    # 도둑이 활성화 상태에서의 동작
    elif thief_active and not out:
        # 도둑이 캐릭터를 따라다님
        dx = character_rect.centerx - thief_rect.centerx
        dy = character_rect.centery - thief_rect.centery
        distance = pygame.math.Vector2(dx, dy).length()
        if distance != 0:
            speed_factor = 0.0002
            thief_rect.x += dx * speed_factor * distance
            thief_rect.y += dy * speed_factor * distance

            if current_time - thief_timer >= 5000:
                out = True
        if character_rect.colliderect(thief_rect):
            score -= 10


    elif out:
        # 화면 밖으로 이동
        dx = width 
        dy = height
        distance = pygame.math.Vector2(dx, dy).length()

        if thief_rect.x < width and thief_rect.y < width:
            speed_factor = 0.0001
            thief_rect.x += dx * speed_factor * distance
            thief_rect.y += dy * speed_factor * distance

        else:
            thief_active = False
            last_time = pygame.time.get_ticks()
            out = False



    # 배경 그리기
    screen.blit(background_image, (0, 0))
                

    # 캐릭터 그리기
    screen.blit(character_img, character_rect)

    # 아이템 그리기
    for item_type, item_rect in items:
        if item_type == 1:
            screen.blit(item1_img, item_rect.topleft)
        else:
            screen.blit(item2_img, item_rect.topleft)

    # 도둑 그리기 (활성화 상태일 때)
    if thief_active:
        screen.blit(thief_img, thief_rect.topleft)

    # 메뉴 아이콘 그리기
    if not menu_active: 
        screen.blit(menu_icon_img, menu_icon_rect)
    
    # 메뉴 화면 그리기
    if menu_active:     
        pygame.draw.rect(screen, (255, 255, 255), menu_rect)

        screen.blit(back_icon_img, back_icon_rect.topleft)

        menu_text = font.render("MENU", True, (0, 0, 0))
        screen.blit(menu_text, (width // 2 - menu_text.get_width() // 2, 170))
        
        screen.blit(menu_button1_img, menu_button1_rect)
        screen.blit(menu_button2_img, menu_button2_rect)
        screen.blit(menu_button3_img, menu_button3_rect)
        screen.blit(menu_button4_img, menu_button4_rect)
        
    # 잔고 표시
    pygame.draw.rect(screen, (255, 227, 0), ((width - 206, 0), (250, 40)))
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"{score}", True, (0, 0, 0))
    screen.blit(score_text, (width - 200, 10))

    if score >= 0:
        end_game()

    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
sys.exit()
