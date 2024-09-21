import pygame
import sys
import os

score = 0

def Arbeit(score):

    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("아르바이트")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    arbeit_background_image_path = os.path.join(current_dir, "../이미지/알바 배경.png")
    arbeit_background_image = pygame.image.load(arbeit_background_image_path)
    arbeit_background_image = pygame.transform.scale(arbeit_background_image, (width, height))

    back_icon_img_path = os.path.join(current_dir, "../이미지/뒤로가기.png")
    back_icon_img = pygame.image.load(back_icon_img_path)  
    back_icon_img = pygame.transform.scale(back_icon_img, (50, 50)) 
    back_icon_rect = back_icon_img.get_rect(topleft=(10, 10))

    character_img_path = os.path.join(current_dir, "../이미지/캐릭터.png")
    character_img = pygame.image.load(character_img_path)
    character_width, character_height = 100, 100
    character_img = pygame.transform.scale(character_img, (character_width, character_height))

    clock = pygame.time.Clock()
    
    gauge_size = (600, 70)
    gauge_position = ((width - gauge_size[0]) // 2, 50)
    
    arbeit_font = pygame.font.Font("C:\WINDOWS\Fonts\gulim.ttc", 60)
    arbeit_text = arbeit_font.render("아무 곳이나 터치!", True, (0, 0, 0))
    arbeit_text_rect = arbeit_text.get_rect(center=(width // 2, 150))

    gauge = 0
    gauge_multiple = 1
    score_multiple = 0

    right = True
    character_x = 0
    
    while True:
        if right:
            screen.blit(arbeit_background_image, (0, 0))
            screen.blit(character_img, (character_x, 500))
            pygame.draw.rect(screen, (189, 189, 189), (gauge_position, gauge_size))
            pygame.draw.rect(screen, (134, 229, 127), (gauge_position, (gauge, 70)))
            screen.blit(back_icon_img, back_icon_rect.topleft)
            screen.blit(arbeit_text, arbeit_text_rect)
            character_x += 4
            if character_x >= 700:
                right = False
                
        elif not right:
            screen.blit(arbeit_background_image, (0, 0))
            screen.blit(character_img, (character_x, 500))
            pygame.draw.rect(screen, (189, 189, 189), (gauge_position, gauge_size))
            pygame.draw.rect(screen, (134, 229, 127), (gauge_position, (gauge, 70)))
            screen.blit(back_icon_img, back_icon_rect.topleft)
            screen.blit(arbeit_text, arbeit_text_rect)
            character_x -= 4
            if character_x <= 0:
                right = True
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_icon_rect.collidepoint(event.pos):
                    return score
                elif gauge < 600:
                    gauge += (60 * gauge_multiple)
                    score += (100 + score_multiple)

                    if gauge >= 600:
                        gauge = 600
                    pygame.draw.rect(screen, (134, 229, 127), (gauge_position, (gauge, 70)))
                    
                elif gauge == 600:
                    pygame.draw.rect(screen, (189, 189, 189), (gauge_position, gauge_size))
                    gauge = 0
                    
                    gauge_multiple *= 0.7
                    score_multiple += 50
                    
        pygame.draw.rect(screen, (255, 227, 0), ((width - 206, 0), (250, 40)))
        score_font = pygame.font.Font(None, 36)                       
        score_text = score_font.render(f"{score}", True, (0, 0, 0))
        screen.blit(score_text, (width - 200, 10))

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    Arbeit(score)
