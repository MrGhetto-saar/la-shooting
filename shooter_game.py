from pygame import *
from random import randint

score = 0
goal = 10
lost = 0
max_lost = 10

font.init()
font1 = font.Font(None, 50)

win_text = font1.render('congrats saar you won this game :)', True, (222, 185, 35))
lose_text = font1.render('Saar you lose saar', True, (235, 59, 5))

class GameSprite(sprite.Sprite):
    def __init__(self, image_file, x, y, widht, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_file), (widht,height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < win_widht-65:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_widht-80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_height = 500
win_widht = 700
main_win = display.set_mode((win_widht, win_height))
display.set_caption('Shooter Game')

background = transform.scale(image.load('windows_xp.jpeg'), (win_widht, win_height))
player = Player('bilo.jpeg', 310, 400, 80, 100, 6)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png',  randint(0, win_widht-80), -40, 90, 60, randint(1,3))
    asteroids.add(asteroid) 

monsters = sprite.Group()
for i in range(3):
    monster = Enemy('Mmmmm_plastic.jpg', randint(0, win_widht-80), -40, 90, 60, randint(1,3))
    monsters.add(monster)

bullets = sprite.Group()

#masukin musik
mixer.init()
mixer.music.load('bosnov-ringtone.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

game_status = True
clock = time.Clock()
FPS = 60
finish = False
life = 3 

while game_status:
    for e in event.get():
        if e.type == QUIT:
            game_status = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and  rel_time == False:
                    num_fire += 1 
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

if finish != True:
    if rel_time == True:
        cur_time = timer()

        if cur_time - last_time < 3:
            print("reload")
            reload =  font1.render("Reloading time >:)", 1, (150,0,0))\
            main_win.blit(reload, (260,20))
        else:
            num_fire = 0
        


    if finish != True:
        main_win.blit(background, (0,0))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score += 1
            monster = Enemy('ufo.png', randint(0, win_widht-80), -40, 90, 60, randint(1,3))
            monsters.add(monster)

        text_score = font1.render('Score : ' + str(score), 1, (255, 255, 255))
        main_win.blit(text_score, (10,20))

        text_lost = font1.render('Missed : ' + str(lost), 1, (255, 255, 255))
        main_win.blit(text_lost, (10,50))

        if score >= goal:
            finish = True
            main_win.blit(win_text, (150,245))


        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            life -=1
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)

            if lost >= max_lost or life == 0:
                finish = True
                main_win.blit(lose_text, (150,245))

            if life == 3:
                life_color = (0,150,0)
            if life == 2:
                life_color = (150,150,0)
            if life == 1:
                life_color = (150,0,0)

            text_life = font1.render(str(life), 1, life_color)
            main_win.blit(text_life, (650,30))


        if lost >= max_lost or sprite.spritecollide(player, monsters, False):
            finish = True
            main_win.blit(lose_text, (150,245))

        player.update()
        player.reset()

        monsters.draw(main_win)
        monsters.update()

        bullets.update()
        bullets.draw(main_win)

    else:
        finish = False
        score = 0
        lose = 0
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()

        time.delay(3000)
        for i in range(1, 3):
            monster = Enemy('ufo.png', randint(0, win_widht-80), -40, 90, 60, randint(1,3))
            monsters.add(monster)


    display.update()
    clock.tick(FPS)
