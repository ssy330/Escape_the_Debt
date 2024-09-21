import pygame
import os
import random
import sys
import tkinter as tk
from tkinter.simpledialog import askinteger
from tkinter import messagebox

dummy_root = tk.Tk()
dummy_root.withdraw()

score = 0

# 이미지 로드
current_dir = os.path.dirname(os.path.abspath(__file__))
back_icon_img_path = os.path.join(current_dir, "../이미지/뒤로가기.png")
back_icon_img = pygame.image.load(back_icon_img_path)  
back_icon_img = pygame.transform.scale(back_icon_img, (50, 50)) 
back_icon_rect = back_icon_img.get_rect(topleft=(10, 10))

def get_horse_number():
    return askinteger("말 번호 선택", "1에서 8까지의 말 번호를 선택하세요", minvalue=1, maxvalue=8)

def get_bet_amount():
    return askinteger("배팅 금액 입력", "배팅할 금액을 입력하세요", minvalue=1)

def reset_game():
    global run_race, result

    run_race = False
    chosen_horse_number = None
    bet_amount = 0

def move_horses_to_start(horses):
    for horse in horses:
        horse["position"] = 0
        horse["x"] = 50

def show_winner_message(winner_name1, winner_name2, winner_name3):
    messagebox.showinfo("승리", f"1등 : {winner_name1}\n 2등 : {winner_name2}\n 3등 : {winner_name3}")
    
def Horse_game(score):
    global chosen_horse_number, run_race, start_time, bet_amount
    
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Horse Race Game")

    horse_background_img_path = os.path.join(current_dir, "../이미지/경마장 배경.png")
    horse_background_img = pygame.image.load(horse_background_img_path)
    horse_background_img = pygame.transform.scale(horse_background_img, (width, height))

    clock = pygame.time.Clock()

    horses = []

    horse_img_path = os.path.join(current_dir, "../이미지/말.png")
    for i in range(8):
        horse = {"name": f"{i + 1}번", "x": 50, "y": i * 52 + 50, "position": 0, "img": pygame.image.load(horse_img_path)}
        horses.append(horse)

    start_button_rect = pygame.Rect(300, 500, 100, 50)
    start_button_color = (0, 255, 0)

    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_icon_rect.collidepoint(event.pos):
                    return score
                elif not run_race and start_button_rect.collidepoint(event.pos):
                    chosen_horse_number = get_horse_number()
                    if chosen_horse_number is not None:
                        bet_amount = get_bet_amount()
                        if bet_amount is not None:
                            score -= bet_amount
                            reset_game()
                            move_horses_to_start(horses) 
                            run_race = True
                     
        screen.blit(horse_background_img, (0, 0))
        screen.blit(back_icon_img, back_icon_rect.topleft)
        
        for horse in horses:
            screen.blit(horse["img"], (horse["x"], horse["y"]))
            font = pygame.font.Font("C:\WINDOWS\Fonts\gulim.ttc", 20)
            text = font.render(horse["name"], True, (0, 0, 0))
            screen.blit(text, (horse["x"]-40, horse["y"] + 40))

        if not run_race:
            pygame.draw.rect(screen, start_button_color, start_button_rect)
            font = pygame.font.Font("C:\WINDOWS\Fonts\gulim.ttc", 20)
            text = font.render("Start", True, (0, 0, 0))
            screen.blit(text, (330, 515))
        else:
            for horse in horses:
                distance = random.uniform(0.0, 2.0)

                if 0 <= horse["position"] < 110:
                    speed = random.uniform(0, 6) 
                elif 110 <= horse["position"] < 220:
                    speed = random.uniform(0, 6)
                elif 220 <= horse["position"] < 330:
                    speed = random.uniform(0, 6)
                elif 330 <= horse["position"] < 440:
                    speed = random.uniform(0, 6)
                elif 440 <= horse["position"]:
                    speed = random.uniform(0, 6)

                horse["position"] += distance * speed
                horse["x"] += distance * speed

            for horse in horses:
                screen.blit(horse["img"], (horse["x"], horse["y"]))
                font = pygame.font.Font("C:\WINDOWS\Fonts\gulim.ttc", 20)
                text = font.render(horse["name"], True, (0, 0, 0))
                screen.blit(text, (horse["x"]-40, horse["y"] + 40))

            if any(horse["position"] >= 550 for horse in horses):
                run_race = False
                winners = sorted(horses, key=lambda x: x["position"], reverse=True)
                if chosen_horse_number is not None and chosen_horse_number == int(winners[0]["name"][:-1]):
                    score += bet_amount * 10
                elif chosen_horse_number is not None and chosen_horse_number == int(winners[1]["name"][:-1]):
                    score += bet_amount * 5
                elif chosen_horse_number is not None and chosen_horse_number == int(winners[2]["name"][:-1]):
                    score += bet_amount * 3
                show_winner_message(winners[0]['name'], winners[1]['name'], winners[2]['name'])
                
                reset_game()
                move_horses_to_start(horses) 
                    

        # 잔고 표시
        pygame.draw.rect(screen, (255, 227, 0), ((width - 206, 0), (250, 40)))
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"{score}", True, (0, 0, 0))
        screen.blit(score_text, (width - 200, 10))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    Horse_game(score)

