import random
import itertools
import sys
import math
import pygame
from pygame.locals import *

class ReversiSystem:
    def __init__(self, surface, x=0, y=0, width=720, height=720, board_size=8):
        self.clean_board()
        self.set_board_size_rect(surface, x, y, width, height)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.pitch_x = (self.width - self.x) / self.board_size
        self.pitch_y = (self.height - self.y) / self.board_size
        self.pass_count = 0

    # 盤面をリセット
    def clean_board(self, board_size=8):
        self.board_size = board_size
        self.board = [[0] * self.board_size for i in range(self.board_size)]
        self.board[int(self.board_size/2-1)][int(self.board_size/2-1)] = 1
        self.board[int(self.board_size/2  )][int(self.board_size/2  )] = 1
        self.board[int(self.board_size/2-1)][int(self.board_size/2  )] = 2
        self.board[int(self.board_size/2  )][int(self.board_size/2-1)] = 2

    # 盤面の大きさを設定
    def set_board_size_rect(self, surface, x, y, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.pitch_x = (width - x) / self.board_size
        self.pitch_y = (height - y) / self.board_size

    # 盤面表示関数
    def draw_board(self):
        self.surface.fill((33, 115, 55))
        for i in range(self.board_size):
            for j in range(self.board_size):
                pygame.draw.rect(self.surface, (0, 0, 0), (self.x+i*self.pitch_x,self.y+j*self.pitch_y,self.pitch_x,self.pitch_y), 2)
                if self.board[i][j] == 1:
                    pygame.draw.circle(self.surface, (0, 0, 0), (int(self.x+i*self.pitch_x+(self.pitch_x/2)),int(self.y+j*self.pitch_y+(self.pitch_y/2))), int((self.pitch_x+self.pitch_y)*0.2))
                elif self.board[i][j] == 2:
                    pygame.draw.circle(self.surface, (255, 255, 255), (int(self.x+i*self.pitch_x+(self.pitch_x/2)),int(self.y+j*self.pitch_y+(self.pitch_y/2))), int((self.pitch_x+self.pitch_y)*0.2))

    # クリック場所取得関数
    def get_mouse_board_area(self):
        x, y = pygame.mouse.get_pos()
        return (math.floor(x / ((self.width - self.x) / self.board_size)), math.floor(y / ((self.height - self.y) / self.board_size)))
    
    # 石を設置可能な場所を取得
    def get_settable_point(self, id):
        settable_point = [[0] * self.board_size for i in range(self.board_size)]
        if not (id == 1 or id == 2):
            return settable_point
        else:
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.board[i][j] != 0:
                        settable_point[i][j] = 0
                    else:
                        for k in range(-1,2):
                            for l in range(-1,2):
                                if not (k == 0 and l == 0):
                                    n = 0
                                    while 1:
                                        if i+k*(n+1) < 0 or j+l*(n+1) < 0 or i+k*(n+1) > self.board_size-1 or j+l*(n+1) > self.board_size-1:
                                            break
                                        if id == 1:
                                            if self.board[i+k*(n+1)][j+l*(n+1)] == 2:
                                                n = n + 1
                                            elif self.board[i+k*(n+1)][j+l*(n+1)] == 1 and n >= 1:
                                                settable_point[i][j] = 1
                                                break
                                            else:
                                                break
                                        elif id == 2:
                                            if self.board[i+k*(n+1)][j+l*(n+1)] == 1:
                                                n = n + 1
                                            elif self.board[i+k*(n+1)][j+l*(n+1)] == 2 and n >= 1:
                                                settable_point[i][j] = 1
                                                break
                                            else:
                                                break
        return settable_point

    # 石を設置可能か取得
    def can_set_new_point(self, id):
        if self.get_settable_point(id) == [[0] * self.board_size for i in range(self.board_size)]:
            return False
        else:
            return True

    # 石を設置可能な場所を描画
    def draw_settable_point(self, id, color_active = (204, 255, 212), color_negative = (135, 168, 140)):
        board = self.get_settable_point(id)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 1:
                    if (i,j) == self.get_mouse_board_area():
                        color = color_active
                    else:
                        color = color_negative
                    pygame.draw.circle(self.surface, color, (int(self.x+i*self.pitch_x+(self.pitch_x/2)),int(self.y+j*self.pitch_y+(self.pitch_y/2))), int((self.pitch_x+self.pitch_y)*0.2),5)

    # 新しい石を設置
    def set_new_point(self, id, x, y):
        if not (id == 1 or id == 2):
            return
        else:
            if self.board[x][y] == 0:
                for k in range(-1,2):
                    for l in range(-1,2):
                        if not (k == 0 and l == 0):
                            n = 0
                            while 1:
                                if x+k*(n+1) < 0 or y+l*(n+1) < 0 or x+k*(n+1) > self.board_size-1 or y+l*(n+1) > self.board_size-1:
                                    break
                                if id == 1:
                                    if self.board[x+k*(n+1)][y+l*(n+1)] == 2:
                                        n = n + 1
                                    elif self.board[x+k*(n+1)][y+l*(n+1)] == 1 and n >= 1:
                                        for i in range(n):
                                            self.board[x+k*(i+1)][y+l*(i+1)] = 1
                                        break
                                    else:
                                        break
                                elif (id == 2):
                                    if self.board[x+k*(n+1)][y+l*(n+1)] == 1:
                                        n = n + 1
                                    elif self.board[x+k*(n+1)][y+l*(n+1)] == 2 and n >= 1:
                                        for i in range(n):
                                            self.board[x+k*(i+1)][y+l*(i+1)] = 2
                                        break
                                    else:
                                        break
        self.board[x][y] = id

    #プレイヤーの入力を待機(id=1:黒, id=2:白)
    def standby_player_input(self, events, id):
        res = 0
        if self.can_set_new_point(id) == False and self.pass_count < 2:
            self.pass_count = self.pass_count + 1
            return 2
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                x, y = self.get_mouse_board_area()
                if self.get_settable_point(id)[x][y] == 1:
                    self.set_new_point(id, x, y)
                    self.pass_count = 0
                    res = 1
        if self.check_end_game() == True:
            res = 3
        return res

    # 石の数を確認する関数(id=1:黒, id=2:白)
    def count(self, id):
        n = 0
        for board_list in self.board:
            n = n + board_list.count(id)
        return n

    # コンピューターの入力を待機
    def standby_computer_input(self, id, callback, wait_seconds = 0.5):
        pygame.time.wait(int(wait_seconds * 1000))
        if self.can_set_new_point(id) == False and self.pass_count < 2:
            self.pass_count = self.pass_count + 1
            return 2
        settable_point = self.get_settable_point(id)
        (x, y) = callback(self, id, self.board, settable_point)
        if settable_point[x][y] == 1:
            self.set_new_point(id, x, y)
            self.pass_count = 0
        if self.check_end_game() == True:
            return 3
        return 1

    # ゲーム終了確認
    def check_end_game(self):
        #print(self.count(1) + self.count(2))
        if self.pass_count >= 2 or self.count(1) + self.count(2) >= self.board_size ** 2:
            return True
        else:
            return False
        
# コンピュータープレイヤー
def computer_test_player(reversi_system, id, board, settable_point):
    settable_point_buf = list(itertools.chain.from_iterable(settable_point))
    rand = random.randint(0,settable_point_buf.count(1)-1)
    n = [i for i, x in enumerate(settable_point_buf) if x == 1][rand]
    x = math.floor(n / reversi_system.board_size)
    y = n - x * reversi_system.board_size
    return (x, y) 

def get_pygame_transparent_surface(width, height, color):
    surface = pygame.Surface((width,height),flags=pygame.SRCALPHA)
    surface.fill(color)
    return surface

def main():
    # 初期化
    pygame.init()
    surface = pygame.display.set_mode((720, 720)) 
    pygame.display.set_caption("Pygame Reversi Sample")
    clock = pygame.time.Clock()
    rs = ReversiSystem(surface, 0, 0, 720, 720)
    font = (pygame.font.Font(None, 55), pygame.font.Font(None, 40), pygame.font.Font(None, 100))
    
    # 状態管理変数
    event_state = 0
    # ループ続行フラグ
    isRunning = True
    # パス用フラグ
    pass_timer = 0
    # 待機用フラグ
    wait_timer = 0
    # プレイヤー, NPC変更用変数(1:プレイヤー, 2:NPC)
    player1 = "player"
    player2 = "player"

    # メインループ
    while isRunning:
        # イベントを取得
        events = pygame.event.get()
        for event in events:
            # 終了イベント処理
            if event.type == pygame.QUIT:
                isRunning = False
 
        # 盤面描画
        rs.draw_board()

        # パスを確認
        if pass_timer > 0:
            #pygame.time.wait(pass_timer)
            surface.blit(get_pygame_transparent_surface(720, 720, (0, 0, 0, 127)),[0, 0])
            surface.blit(font[2].render("Pass", True, (255,255,255)), [20, 20])
            pass_timer = pass_timer - 1
        elif wait_timer > 0:
            wait_timer = wait_timer - 1
        else:
            # スタート画面
            if event_state == 0:
                # 半透明背景
                surface.blit(get_pygame_transparent_surface(720, 720, (0, 0, 0, 127)),[0, 0])
                # 文字列
                surface.blit(font[0].render("Reversi", True, (255,255,255)), [20, 20])
                surface.blit(font[1].render("Left Click - PvP", True, (255,255,255)), [20, 80])
                surface.blit(font[1].render("Right Click - PvE", True, (255,255,255)), [20, 120])
                surface.blit(font[1].render("Center Click - EvE", True, (255,255,255)), [20, 160])
                for event in events:
                    if event.type == MOUSEBUTTONDOWN:
                        print(event.button)
                        event_state = 1
                        pygame.display.set_caption("Pygame Reversi Sample [Player1:Black]")
                        if event.button == 1:
                            player1 = "player"
                            player2 = "player"
                        elif event.button == 3:
                            player1 = "player"
                            player2 = "computer"
                        else:
                            player1 = "computer"
                            player2 = "computer"

            # プレイヤー1のターン
            elif event_state == 1:
                if player1 == "player":
                    rs.draw_settable_point(1)
                    input_state = rs.standby_player_input(events, 1)
                else:
                    input_state = rs.standby_computer_input(1, computer_test_player, 0)
                if input_state == 1 or input_state == 2:
                    if input_state == 2 and (player1 == "player" or player2 == "player"):
                        pass_timer = 60
                    if player2 != "player"and (player1 == "player" or player2 == "player"):
                        wait_timer = 40
                    event_state = 2
                    pygame.display.set_caption("Pygame Reversi Sample [Player2:White]")
                elif input_state == 3:
                    event_state = -1
                    pygame.display.set_caption("Pygame Reversi Sample")

            # プレイヤー2のターン
            elif event_state == 2:
                if player2 == "player":
                    rs.draw_settable_point(2)
                    input_state = rs.standby_player_input(events, 2)
                else:
                    input_state = rs.standby_computer_input(2, computer_test_player, 0)
                if input_state == 1 or input_state == 2:
                    if input_state == 2 and (player1 == "player" or player2 == "player"):
                        pass_timer = 60
                    if player1 != "player" and (player1 == "player" or player2 == "player"):
                        wait_timer = 40
                    event_state = 1
                    pygame.display.set_caption("Pygame Reversi Sample [Player1:Black]")
                elif input_state == 3:
                    event_state = -1
                    pygame.display.set_caption("Pygame Reversi Sample")

            # ゲーム終了
            elif event_state == -1:
                # 半透明背景
                surface.blit(get_pygame_transparent_surface(720, 720, (0, 0, 0, 127)),[0, 0])
                # 文字列
                if rs.count(1) > rs.count(2):
                    text = "Black Win! (Black:" + str(rs.count(1)) + ", White:" + str(rs.count(2)) + ")"
                elif rs.count(1) < rs.count(2):
                    text = "White Win! (Black:" + str(rs.count(1)) + ", White:" + str(rs.count(2)) + ")"
                else:
                    text = "Draw (Black:" + str(rs.count(1)) + ", White:" + str(rs.count(2)) + ")"
                surface.blit(font[0].render(text, True, (255,255,255)), [20, 20])
                surface.blit(font[1].render("Left Click - PvP", True, (255,255,255)), [20, 80])
                surface.blit(font[1].render("Right Click - PvE", True, (255,255,255)), [20, 120])
                surface.blit(font[1].render("Center Click - EvE", True, (255,255,255)), [20, 160])
                for event in events:
                    if event.type == MOUSEBUTTONDOWN:
                        event_state = 1
                        rs.clean_board()
                        pygame.display.set_caption("Pygame Reversi Sample [Player1:Black]")
                        if event.button == 1:
                            player1 = "player"
                            player2 = "player"
                        elif event.button == 3:
                            player1 = "player"
                            player2 = "computer"
                        else:
                            player1 = "computer"

        # メイン画面の更新
        pygame.display.update()

        # フレームレートの設定
        clock.tick(60)

    # 終了処理
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
