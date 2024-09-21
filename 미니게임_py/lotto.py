import pygame
import sys
import random
import os

score = 0

def Lotto(score):
    # Pygame 초기화
    pygame.init()

    # 화면 설정
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("로또")

    # 이미지 로드
    current_dir = os.path.dirname(os.path.abspath(__file__))
    back_icon_img_path = os.path.join(current_dir, "../이미지/뒤로가기.png")
    back_icon_img = pygame.image.load(back_icon_img_path)
    back_icon_img = pygame.transform.scale(back_icon_img, (50, 50))
    back_icon_rect = back_icon_img.get_rect(topleft=(10, 10))

    # 입력 상자 생성
    input_boxes = [pygame.Rect(86 + i * 110, 200, 80, 80) for i in range(6)]
    user_numbers = [0] * 6

    # 확인 버튼
    check_button = pygame.Rect(350, 500, 100, 50)

    # 결과 텍스트
    your_number_text = ""
    lotto_number_text = ""
    result_text = ""

    # 시간 초기화
    lotto_start_time = 0  
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_icon_rect.collidepoint(event.pos):
                    return score
                for i, box in enumerate(input_boxes):
                    expanded_box = pygame.Rect(box.x - 10, box.y - 40, box.width + 10, box.height + 70)
                    if expanded_box.collidepoint(event.pos):
                        if event.pos[1] > box.y + box.height / 2:
                            user_numbers[i] = (user_numbers[i] - 1) % 10
                        else:
                            user_numbers[i] = (user_numbers[i] + 1) % 10
                if check_button.collidepoint(event.pos):
                    score -= 1000
                    generated_numbers = sorted(random.sample(range(0, 10), 6))
                    count = len(set(user_numbers) & set(generated_numbers))
                    your_number_text = f"선택한 번호: {user_numbers}"
                    lotto_number_text = f"로또 번호: {generated_numbers}"
                    result_text = f"맞은 개수: {count}"
                    lotto_start_time = pygame.time.get_ticks()
                    if count == 6:
                        score += 1000000
                    elif count == 5:
                        score += 500000
                    elif count == 4:
                        score += 300000

        # 화면 업데이트
        screen.fill((255, 255, 255))
        screen.blit(back_icon_img, back_icon_rect.topleft)

        for i, box in enumerate(input_boxes):
            # 숫자에 따라 색상 지정
            number_color = (0, 0, 0) 
            if 0 <= user_numbers[i] <= 1:
                number_color = (225, 228, 0)
            elif 2 <= user_numbers[i] <= 3:
                number_color = (67, 116, 217)
            elif 4 <= user_numbers[i] <= 6:
                number_color = (214, 61, 61)
            elif 7 <= user_numbers[i] <= 9:
                number_color = (140, 140, 140)

            # 로또 공 그리기
            pygame.draw.ellipse(screen, number_color, box)  
            pygame.draw.ellipse(screen, (0, 0, 0), box, 2) 
            number_font = pygame.font.Font(None, 36)
            number_text = number_font.render(str(user_numbers[i]), True, (255, 255, 255)) 
            screen.blit(number_text, (box.x + 35 - number_text.get_width() // 2, box.y + 40 - number_text.get_height() // 2))

        # 결과를 화면 중앙에 표시함
        if lotto_start_time > 0:
            elapsed_time = pygame.time.get_ticks() - lotto_start_time
            if elapsed_time < 5000:
                lotto_rect = pygame.Rect(100, 150, 600, 300)
                pygame.draw.rect(screen, (218, 217, 255), lotto_rect)

                font = pygame.font.Font("C:/WINDOWS/Fonts/gulim.ttc", 36)
                result_surface1 = font.render(f"{your_number_text}", True, (0, 0, 0))
                screen.blit(result_surface1, (width // 2 - result_surface1.get_width() // 2, height // 2 - result_surface1.get_height() // 2 - 50))

                result_surface2 = font.render(f"{lotto_number_text}", True, (0, 0, 0))
                screen.blit(result_surface2, (width // 2 - result_surface2.get_width() // 2, height // 2 - result_surface2.get_height() // 2))

                result_surface3 = font.render(f"{result_text}", True, (0, 0, 0))
                screen.blit(result_surface3, (width // 2 - result_surface3.get_width() // 2, height // 2 - result_surface3.get_height() // 2 + 50))
            else:
                # 5초가 지나면 초기 상태로 돌아감
                your_number_text = ""
                lotto_number_text = ""
                result_text = ""
                lotto_start_time = 0
                user_numbers = [0] * 6

        # 버튼과 잔고 창 그리기
        pygame.draw.rect(screen, (0, 255, 0), check_button)
        check_text = number_font.render("result", True, (0, 0, 0))
        screen.blit(check_text, (check_button.x + 16, check_button.y + 14))

        pygame.draw.rect(screen, (255, 227, 0), ((width - 206, 0), (250, 40)))
        score_font = pygame.font.Font(None, 36)                       
        score_text = score_font.render(f"{score}", True, (0, 0, 0))
        screen.blit(score_text, (width - 200, 10))
        
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    Lotto(score)



