import pygame
import random

pygame.init()

LEBAR_SCENE = 500
TINGGI_SCENE = 600
JUDUL_SCENE = "Game para gengster"
GAMBAR_BACKGROUND = "grass.jpg"
GAMBAR_PEMAIN1 = "bilo.jpeg"
GAMBAR_MUSUH1 = "Mmmmm_plastic.jpg"
MUSIK_BACKGROUND = "bosnov_ringtone.mp3"
GAME_ON = True 
GAME_FINISH = False 
JUMLAH_MUSUH = 5
POIN = 0
LEWAT = 0
WARNA_PUTIH = (255, 255, 255)
WARNA_HITAM = (0, 0, 0)

SCENE = pygame.display.set_mode((LEBAR_SCENE, TINGGI_SCENE))
pygame.display.set_caption(JUDUL_SCENE)
BACKGROUND = pygame.transform.scale(pygame.image.load(GAMBAR_BACKGROUND),
    (LEBAR_SCENE, TINGGI_SCENE))

pygame.mixer.init()
pygame.mixer.music.load(MUSIK_BACKGROUND)
pygame.mixer.music.play()

pygame.font.init()
FONT1 = pygame.font.Font(None, 34)

class Bullet(GameSprite):
    self.rect.y -= self.kecepatan
    if self.rect.y > 0:
        self.kill()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, gambar, x, y, kecepatan, lebar, tinggi):
        super().__init__()
        self.lebar = lebar
        self.tinggi = tinggi
        self.gambar = pygame.transform.scale(pygame.image.load(gambar), (self.lebar, self.tinggi))    
        self.kecepatan = kecepatan
        self.rect = self.gambar.get_rect()
        self.rect.x = x
        self.rect.y = y 
    def tampil(self):
        SCENE.blit(self.gambar, (self.rect.x, self.rect.y-self.tinggi))
    def tembak(self):
        PELURU = Bullet(GAMBAR_PERLURU, self.rect.x+40, self.rect.y-50, 5, 30,)
        GRUP_PELURU.add(PELURU)

class Player(GameSprite):
    def update(self):
        TOMBOL = pygame.key.get_pressed()
        if TOMBOL[pygame.K_a] and self.rect.x > 0: # kekiri
            self.rect.x -= self.kecepatan
        if TOMBOL[pygame.K_d] and self.rect.x < LEBAR_SCENE-self.lebar: # kekanan
            self.rect.x += self.kecepatan
class Enemy(GameSprite):
    def update(self):
        global LEWAT
        self.rect.y += self.kecepatan
        if self.rect.y > TINGGI_SCENE:
            LEWAT += 1
            self.rect.y = -self.tinggi
            self.rect.x = random.randint(50, LEBAR_SCENE-self.lebar)

PEMAIN1 = Player(GAMBAR_PEMAIN1, 100, TINGGI_SCENE, 20, 150, 150)

GRUP_MUSUH = pygame.sprite.Group()
for a in range(JUMLAH_MUSUH):
    MUSUH1 = Enemy(GAMBAR_MUSUH1, random.randint(50, LEBAR_SCENE-200), -100,
        random.randint(1,7), 100, 100)
    GRUP_MUSUH.add(MUSUH1)



GRUP_PELURU = pygame.sprite.Group()

while GAME_ON:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_ON = False 
    
    if GAME_FINISH == False:
        SCENE.blit(BACKGROUND, (0, 0))
        PEMAIN1.tampil()
        
        tulisan_poin = FONT1.render("POIN : " + str(POIN), True, WARNA_HITAM)
        tulisan_lewat = FONT1.render("LEWAT : " + str(LEWAT), True, WARNA_HITAM)
        SCENE.blit(tulisan_poin, (10, 10))
        SCENE.blit(tulisan_lewat, (10, 60))

        for musuh in GRUP_MUSUH:
            musuh.tampil()

        PEMAIN1.update()
        GRUP_MUSUH.update()

    pygame.display.update()
