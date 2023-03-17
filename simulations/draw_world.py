import pygame

def main():
  pygame.init()
  screen = pygame.display.set_mode((900, 900))
  pygame.display.set_caption("My Pygame Window")
  clock = pygame.time.Clock()

  running = True
  c = 0
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (320, 240), 50)
    pygame.draw.rect(screen, (255, 0, 0), (850, 20, 30, 30), 50)
    pygame.display.update()

    clock.tick(60)
    c += 1

  pygame.quit()

if __name__ == '__main__':
    main()
