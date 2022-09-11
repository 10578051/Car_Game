import pygame

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_Left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_Left).center)
    win.blit(rotated_image, new_rect.topleft)

#The following is to show text on the screen
def blit_text_center(win, font, text):
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))

#Source of the above code https://www.youtube.com/watch?v=L3ktUWfAMPg&t=1267s&ab_channel=TechWithTim