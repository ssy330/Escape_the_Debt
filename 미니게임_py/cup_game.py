import sys
import random
import pygame
import os

score = 0

def Cup_game(score):
    shuffle = 0
    ready = False
    cups_y1 = 100
    cups_y2 = 300

    # Pygame 초기화
    pygame.init()

    # 화면 설정
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("../이미지/구슬 찾기 게임")

    # 이미지 로드
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cup_image_path = os.path.join(current_dir, "../이미지/컵.png")
    cup_image = pygame.image.load(cup_image_path)
    cup_image = pygame.transform.scale(cup_image, (100, 150))

    bead_image_path = os.path.join(current_dir, "../이미지/구슬.png")
    bead_image = pygame.image.load(bead_image_path)
    bead_image = pygame.transform.scale(bead_image, (50, 50))

    button_image_path = os.path.join(current_dir, "../이미지/버튼.png")
    button_image = pygame.image.load(button_image_path)
    button_image = pygame.transform.scale(button_image, (150, 100))
    button_rect = button_image.get_rect(center=(width//2, 500))

    back_icon_img_path = os.path.join(current_dir, "../이미지/뒤로가기.png")
    back_icon_img = pygame.image.load(back_icon_img_path)  
    back_icon_img = pygame.transform.scale(back_icon_img, (50, 50)) 
    back_icon_rect = back_icon_img.get_rect(topleft=(10, 10))
    
    # 초기 위치
    cup_rect = cup_image.get_rect(topleft=(100, 800))
    bead_x_list = [178, 378, 578]
    bead_x = random.choice(bead_x_list)
    bead_rect = pygame.Rect(bead_x, 380, 50, 50)

    # Clock 객체 생성
    clock = pygame.time.Clock()

    # 컵 리스트 생성
    cups = [{"image": cup_image, "rect": cup_rect.copy(), "x": 150, "has_bead": 0}, 
            {"image": cup_image, "rect": cup_rect.copy(), "x": 350, "has_bead": 0},
            {"image": cup_image, "rect": cup_rect.copy(), "x": 550, "has_bead": 0}]

    cups[bead_x_list.index(bead_x)]["has_bead"] = 1


    # 목적지 리스트 생성
    destinations = [[random.choice([100, 300, 500]) for _ in range(10)] for _ in range(3)]
    shuffled_values = [150, 350, 550]
    random.shuffle(shuffled_values)
    destinations[0][9], destinations[1][9], destinations[2][9] = shuffled_values  # 마지막에 컵의 위치가 중복되지 않도록

    # 목적지 변경 횟수
    destination_changes = [0, 0, 0]

    # 게임 루프
    answer = None 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_icon_rect.collidepoint(event.pos):
                    return score


        # 화면 채우기
        screen.fill((255, 255, 255))
        screen.blit(back_icon_img, back_icon_rect.topleft)
                
        if shuffle == 0:
            for cup in cups:
                screen.blit(cup["image"], (cup["x"], 100))
            screen.blit(bead_image, (bead_rect[0], bead_rect[1]))
            screen.blit(button_image, button_image.get_rect(center=(width//2, 500)))
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    score -= 500
                    shuffle = 1
                    ready = True  
                    
                    
        if shuffle == 1:
            screen.blit(bead_image, (bead_rect[0], bead_rect[1]))      
            if cups_y1 < 300:
                cups_y1 += 2
                for cup in cups:
                    screen.blit(cup["image"], (cup["x"], cups_y1))
            else:
                shuffle = 2

        if shuffle == 2:
            all_cups_at_destination = all(destination_changes[i] >= len(destinations[i]) for i in range(3))

            if all_cups_at_destination:
                shuffle = 3
                
            for i in range(3):
                if destination_changes[i] < len(destinations[i]):
                    destination = destinations[i][destination_changes[i]]
                    if cups[i]["x"] != destination:
                        if cups[i]["x"] < destination:
                            cups[i]["x"] += 5
                        elif cups[i]["x"] > destination:
                            cups[i]["x"] -= 5
                    else:
                        # 목적지에 도착한 경우 목적지 변경
                        destination_changes[i] += 1

                for cup in cups:
                    screen.blit(cup["image"], (cup["x"], 300))
                    
        if shuffle == 3:
            for cup in cups:
                screen.blit(cup["image"], (cup["x"], 300))
                

            if event.type == pygame.MOUSEBUTTONUP:
                Mx, My = pygame.mouse.get_pos()
                if 150 < Mx < 250 and 285 < My < 450:
                    for _ in range(3):
                        if cups[_].get("x") == 150:
                            answer = _
                            shuffle = 4
                elif 350 < Mx < 450 and 285 < My < 450:
                    for _ in range(3):
                        if cups[_].get("x") == 350:
                            answer = _
                            shuffle = 4
                elif 550 < Mx < 650 and 285 < My < 450:
                    for _ in range(3):
                        if cups[_].get("x") == 550:
                            answer = _
                            shuffle = 4
                else:
                    pass

                    
        if shuffle == 4:
            screen.blit(bead_image, (cups[bead_x_list.index(bead_x)]["x"] + 28, bead_rect[1]))
            if answer is not None:
                if cups[answer]["has_bead"] == 1:
                    score += 50
                    font = pygame.font.Font("C:/WINDOWS/Fonts/gulim.ttc", 52)
                    text = font.render("맞았습니다!", True, (0, 0, 0))
                    screen.blit(text, (300, 40))

                elif cups[answer]["has_bead"] == 0:
                    font = pygame.font.Font("C:/WINDOWS/Fonts/gulim.ttc", 52)
                    text = font.render("틀렸습니다!", True, (0, 0, 0))
                    screen.blit(text, (300, 40))

            if cups_y2 > 100:
                cups_y2 -= 2
                for cup in cups:
                    screen.blit(cup["image"], (cup["x"], cups_y2))
            else:
                # 두 번째 판에서 게임 상태 및 변수 초기화
                cups_y1 = 100
                cups_y2 = 300
                shuffle = 0
                ready = False
                destination_changes = [0, 0, 0]
                answer = None
                
                bead_x_list = [178, 378, 578]
                bead_x = random.choice(bead_x_list)
                bead_rect = pygame.Rect(bead_x, 380, 50, 50)
                
                cups = [{"image": cup_image, "rect": cup_rect.copy(), "x": 150, "has_bead": 0}, 
                        {"image": cup_image, "rect": cup_rect.copy(), "x": 350, "has_bead": 0},
                        {"image": cup_image, "rect": cup_rect.copy(), "x": 550, "has_bead": 0}]

                cups[bead_x_list.index(bead_x)]["has_bead"] = 1

                destinations = [[random.choice([100, 300, 500]) for _ in range(10)] for _ in range(3)]
                shuffled_values = [150, 350, 550]
                random.shuffle(shuffled_values)
                destinations[0][9], destinations[1][9], destinations[2][9] = shuffled_values
                
        # 잔고 표시
        pygame.draw.rect(screen, (255, 227, 0), ((width - 206, 0), (250, 40)))
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"{score}", True, (0, 0, 0))
        screen.blit(score_text, (width - 200, 10))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    Cup_game(score)
