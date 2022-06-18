
import pygame
import random
import configparser


class game():
    def __init__(self, m, g, gm, gv, fps):
        self.gm = gm
        self.fps = fps
        self.gv = gv
        self.dgm = gm
        self.dgv = gv
        self.is_music_set = m
        self.is_gmusic_set = g
        self.volume_list = []
        i = 0.0
        while i <= 1.0:
            new = "{:.1f}".format(i)
            i = float(new)
            self.volume_list.append(i)
            i = i+0.1
        self.setvolume()
        self.check_music()
        pygame.init()

        self.window = pygame.display.set_mode((930, 700))
        pygame.display.set_caption("Snake Game by Prathamesh Dhande")
        self.icon_img = pygame.image.load("Images/icon.jpg")
        pygame.display.set_icon(self.icon_img)
        pygame.mixer.init()

        # setting the game variable
        self.yellow = (252, 240, 3)
        self.screen_width = 700
        self.screen_height = 700
        self.exit_game = False
        self.snake_x = 50
        self.snake_y = 50
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = False
        self.red = (255, 0, 0)
        self.count = 0
        self.black = (0, 0, 0)
        self.blue = (80, 138, 156)
        self.snake_length = 1
        self.snake_size = 30
        self.game_over = False
        self.snake_lst = []
        self.cc = 0
        self.white = (255, 255, 255)
        self.highscore = 0
        self.gethighscore()
        self.text = pygame.font.SysFont("Timesnewroman", 60)
        self.pause_text = self.text.render("Paused", True, self.white)

        self.text1 = pygame.font.SysFont("timesnewroman", 40)
        self.notice_text = self.text1.render(
            "Press Arrow Buttons to Continue", True, self.black)

        self.gameover_text = self.text.render("Game Over !", True, self.white)
        self.score = 0

        self.back_img = pygame.image.load("Images/back.jpg")
        self.food_img = pygame.image.load("Images/food.png")

        self.food_x = random.randint(20, 650)
        self.food_y = random.randint(20, 650)
        self.back_img = pygame.transform.scale(
            self.back_img, (self.screen_width, self.screen_height))
        self.food_img = pygame.transform.scale(self.food_img, (27, 35))

        self.clock = pygame.time.Clock()
        try:
            self.__gameloop__()
        except pygame.error as e:
            print(e)

    def screen_placer(self, img, x, y):
        self.window.blit(img, (x, y))

    def screen_collision(self, w, h, x, y):
        if x > w-30 or x < 5:
            self.game_over = True

        elif y > h-40 or y < 8:
            self.game_over = True

    def plot_snake(self, gameWindow, color, snake_lst, snake_size):
        for x, y in snake_lst:
            pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

    def __gameloop__(self):
        while not self.exit_game:

            self.clock.tick(self.fps)
            self.window.fill((255, 255, 255))
            self.screen_placer(self.back_img, 0, 0)

            self.screen_placer(self.food_img, self.food_x, self.food_y)
            if self.game_over:

                self.gameover_screen()
                for self.event in pygame.event.get():
                    if self.event.type == pygame.QUIT:
                        pygame.quit()
                        self.exit_game = True
                        exit()

                    elif self.event.type == pygame.KEYDOWN:
                        if self.event.key == pygame.K_1:
                            self.game_over = False
                            c = game(self.is_music_set, self.is_gmusic_set,
                                     self.dgm, self.dgv, self.fps)

                        elif self.event.key == pygame.K_2:
                            pass

                        elif self.event.key == pygame.K_3:
                            pygame.quit()
                            exit()

            else:

                for self.event in pygame.event.get():
                    if self.event.type == pygame.QUIT:
                        self.exit_game = True
                        exit()
                    if self.event.type == pygame.KEYDOWN:
                        if self.event.key == pygame.K_LEFT:
                            self.velocity_x = -6
                            self.velocity_y = 0

                        elif self.event.key == pygame.K_RIGHT:
                            self.velocity_x = 6
                            self.velocity_y = 0

                        elif self.event.key == pygame.K_UP:
                            self.velocity_x = 0
                            self.velocity_y = -6

                        elif self.event.key == pygame.K_DOWN:
                            self.velocity_x = 0
                            self.velocity_y = 6

                        elif self.event.key == pygame.K_SPACE:
                            self.velocity_x = 0
                            self.velocity_y = 0
                            self.direction = True

                        elif self.event.key == pygame.K_RETURN:
                            self.direction = False

                if self.direction:
                    self.window.fill(self.black)
                    self.screen_placer(self.pause_text, 400, 300)
                    self.retu = self.text1.render(
                        "Press Enter to Return To Game", True, self.yellow)
                    self.screen_placer(self.retu, 250, 390)
                else:
                    self.window.fill((255, 255, 255))
                    self.screen_placer(self.back_img, 0, 0)
                    self.screen_placer(self.food_img, self.food_x, self.food_y)

                self.snake_x += self.velocity_x
                self.snake_y += self.velocity_y
                # print(f"{snake_x} =x and {snake_y} =y")

                self.screen_collision(
                    self.screen_width, self.screen_height, self.snake_x, self.snake_y)

                if abs(self.snake_x-self.food_x) < 15 and abs(self.snake_y-self.food_y) < 16:
                    self.play_gmusic()
                    self.food_x = random.randint(20, 650)
                    self.food_y = random.randint(20, 650)
                    self.snake_length += 5
                    self.score += 5
                self.score_text = self.text1.render(
                    "Score : "+str(self.score), True, self.red)
                self.screen_placer(self.score_text, 725, 50)
                self.text2 = pygame.font.SysFont("timesnewroman", 30)

                self.highscore_placer()

                self.head = []
                self.head.append(self.snake_x)
                self.head.append(self.snake_y)
                self.snake_lst.append(self.head)

                if len(self.snake_lst) > self.snake_length:
                    del self.snake_lst[0]

                if self.head in self.snake_lst[:-1]:
                    self.game_over = True
                # print(snake_lst)
                self.plot_snake(self.window, self.blue,
                                self.snake_lst, self.snake_size)
            pygame.display.update()

    def gameover_screen(self):

        if self.cc == 0:
            self.gameover_music()
            self.cc = 1
        self.window.fill(self.black)
        self.screen_placer(self.gameover_text, 330, 300)
        self.score_text = self.text.render(
            "Score : "+str(self.score), True, self.red)
        self.screen_placer(self.score_text, 370, 60)
        self.play_again = self.text1.render(
            "Press 1 To Play Again", True, self.yellow)
        self.quit = self.text1.render(
            "Press 3 to Exit The Game", True, self.yellow)
        self.screen_placer(self.play_again, 300, 380)
        self.screen_placer(self.quit, 280, 430)

    def mainmenu_gui(self):
        # g=gui.__gui__()
        pygame.quit()

    def check_music(self):
        if self.is_music_set:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.init()
            pygame.mixer.music.load("Sounds/g_music.mp3")
            pygame.mixer.music.set_volume(self.gm)
            pygame.mixer.music.play(-1)

    def play_gmusic(self):
        self.s = pygame.mixer.Sound("Sounds/eat.wav")
        self.s.set_volume(self.gv)
        if self.is_gmusic_set:
            self.s.stop()
        else:
            self.s.play(0)

    def gameover_music(self):
        if self.is_music_set:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Sounds/game_over.mp3")
            pygame.mixer.music.set_volume(self.gm)
            pygame.mixer.music.play(1)

    def setvolume(self):
        self.gv = self.volume_list[self.gv]
        self.gm = self.volume_list[self.gm]

    def gethighscore(self):
        try:
            configuer = configparser.ConfigParser()
            self.read = configuer.read('config.ini')
            self.highscore = configuer['score']['highscore']

        except:
            with open("config.ini", 'w') as f:
                f.write("[score]\nhighscore=0")
            self.highscore = 0

    def highscore_placer(self):

        if int(self.highscore) < self.score:
            self.highscore = self.score
            self.highscore_text = self.text2.render(
                "HighScore : "+str(self.highscore), True, self.black)
            self.screen_placer(self.highscore_text, 710, 100)
            with open("config.ini", 'w') as f:
                f.write(f"[score]\nhighscore={self.highscore}")
        else:
            self.highscore_text = self.text2.render(
                "HighScore : "+str(self.highscore), True, self.black)
            self.screen_placer(self.highscore_text, 710, 100)


if __name__ == "__main__":
    a = False
    b = False
    c = game(a, b, 7, 7, 30)
