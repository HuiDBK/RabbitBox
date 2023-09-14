#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 游戏入口模块 }
# @Date: 2023/09/13 12:20
import sys
import random

import pygame
from pygame import Surface, K_a, K_LEFT, K_d, K_RIGHT, K_w, K_UP, K_s, K_DOWN
from src.game_map import (
    GAME_MAP, WALL_FLAG, PLAYER_FLAG, BOX_FLAG, DEST_FLAG, BG_FLAG,
    EMPTY_FLAG, PLAYER_DEST_FLAG, BOX_DEST_FLAG
)
from src import game_setting
from src.game_setting import MoveDirection


class RabbitBox(object):
    GRID_SIZE = game_setting.GRID_SIZE
    GAME_TITLE = game_setting.GAME_TITLE

    WALLS = game_setting.WALLS
    PLAYERS = game_setting.PLAYERS
    BOXS = game_setting.BOXS
    TERMINAL_BOXS = game_setting.TERMINAL_BOXS
    FINISHED_BOXS = game_setting.FINISHED_BOXS
    BG_BOXS = game_setting.BG_BOXS
    BG_SCREENS = game_setting.BG_SCREENS

    def __init__(self, game_level: int = 1, game_fps=60):
        """
        游戏属性初始化
        Args:
            game_level: 游戏关卡
            game_fps: 游戏帧率
        """
        self._init_game()

        self.game_screen: Surface = None
        self.game_level = min(game_level, len(GAME_MAP))
        self.game_fps = game_fps
        self.player_pos: tuple = None

        self.box: Surface = None
        self.player: Surface = None
        self.wall: Surface = None
        self.terminal_box: Surface = None
        self.finished_box: Surface = None
        self.bg_box: Surface = None
        self.bg_screen: Surface = None

        self.random_game_material()
        self.setup_game_screen()

    def random_game_material(self):
        """随机游戏素材"""
        self.wall = random.choice(self.WALLS)
        self.player = random.choice(self.PLAYERS)
        self.box = random.choice(self.BOXS)
        self.terminal_box = random.choice(self.TERMINAL_BOXS)
        self.finished_box = random.choice(self.FINISHED_BOXS)
        self.bg_box = random.choice(self.BG_BOXS)
        self.bg_screen = random.choice(self.BG_SCREENS)

    def _init_game(self):
        pygame.init()
        pygame.display.set_caption(self.GAME_TITLE)

    def setup_game_screen(self):
        """根据游戏地图配置游戏屏幕"""

        rows = GAME_MAP[self.game_level]
        row_num = len(rows)
        col_num = len(rows[0])

        width = self.GRID_SIZE * row_num
        height = self.GRID_SIZE * col_num
        self.game_screen = pygame.display.set_mode(size=[width, height])

        # 按比例缩放背景图
        self.bg_screen = pygame.transform.scale(self.bg_screen, (width, height))

    def draw_map(self):
        """遍历地图数据绘制"""

        # 获取游戏地图
        game_map = GAME_MAP[self.game_level]

        for i, row in enumerate(game_map):
            for j, col in enumerate(row):

                # 计算偏移坐标
                offset_x = j * self.GRID_SIZE
                offset_y = i * self.GRID_SIZE

                # 判断标识
                num_flag = game_map[i][j]
                if num_flag == WALL_FLAG:
                    # 画墙 （灯笼）
                    self.game_screen.blit(source=self.wall, dest=(offset_x, offset_y))

                elif num_flag in [PLAYER_FLAG, PLAYER_DEST_FLAG]:
                    # 画角色（兔子）
                    self.game_screen.blit(source=self.player, dest=(offset_x, offset_y))
                    self.player_pos = (i, j)  # 标识兔子坐标

                elif num_flag in [BOX_FLAG, BOX_DEST_FLAG]:
                    # 画箱子（月饼）
                    self.game_screen.blit(source=self.box, dest=(offset_x, offset_y))

                elif num_flag == DEST_FLAG:
                    # 画月饼的目的地（月球）
                    self.game_screen.blit(source=self.terminal_box, dest=(offset_x, offset_y))

                # elif num_flag == BG_FLAG:
                #     # 画空（背景）
                #     self.game_screen.blit(source=self.bg_box, dest=(offset_x, offset_y))

        return self.player_pos

    def _handle_player_dest(self):
        """角色和目的地重合处理"""
        i, j = self.player_pos
        map_list = GAME_MAP[self.game_level]
        if map_list[i][j] == PLAYER_DEST_FLAG:
            # 当前位置是角色和目的地重合处理
            map_list[i][j] = DEST_FLAG  # 把原来角色位置改成目的地
        else:
            map_list[i][j] = EMPTY_FLAG  # 把原来角色位置改成空白

    def move_up(self):
        """
        玩家向上移动处理
        """
        print("move_up")

        i, j = self.player_pos
        map_list = GAME_MAP[self.game_level]

        if map_list[i - 1][j] == BOX_FLAG and \
                (map_list[i - 2][j] == EMPTY_FLAG or map_list[i - 2][j] == DEST_FLAG):
            print('up box')
            # 玩家上边(i - 1)是箱子
            # 且箱子的上边只能是空白或者目的地才可向上
            map_list[i - 1][j] = PLAYER_FLAG  # 角色向上移动改变角色位置

            # 角色和目的地重合判断处理
            self._handle_player_dest()

            map_list[i - 2][j] = BOX_FLAG  # 把箱子向上移改变位置

        elif map_list[i - 1][j] == EMPTY_FLAG:
            # 玩家上边(i - 1)是空白
            print('up empty')
            map_list[i - 1][j] = PLAYER_FLAG  # 角色向上移动改变角色位置

            self._handle_player_dest()

        elif map_list[i - 1][j] == DEST_FLAG:
            # 玩家上边是目的地
            print('up destination')
            map_list[i - 1][j] = PLAYER_DEST_FLAG  # 让角色和目的地重合

            self._handle_player_dest()

    def move_down(self):
        """
        玩家向下移动处理
        """
        print("move down")
        i, j = self.player_pos
        map_list = GAME_MAP[self.game_level]

        # 玩家下边(i + 1)是箱子
        # 且箱子的下边只能是空白或者目的地才可向下
        if map_list[i + 1][j] == BOX_FLAG and (map_list[i + 2][j] == EMPTY_FLAG or map_list[i + 2][j] == DEST_FLAG):
            print('down box')
            map_list[i + 1][j] = PLAYER_FLAG  # 角色向下移动改变角色位置
            self._handle_player_dest()
            map_list[i + 2][j] = BOX_FLAG  # 把箱子向下移改变位置

        # 玩家下边(i + 1)是空白
        elif map_list[i + 1][j] == EMPTY_FLAG:
            print('down empty')
            map_list[i + 1][j] = PLAYER_FLAG  # 角色向下移动改变角色位置
            self._handle_player_dest()

        elif map_list[i + 1][j] == DEST_FLAG:
            # 玩家下边是目的地
            print('down destination')
            map_list[i + 1][j] = PLAYER_DEST_FLAG  # 让角色和目的地重合

            self._handle_player_dest()

    def move_lef(self):
        """
        玩家向左移动处理
        """
        print("move left")
        i, j = self.player_pos
        map_list = GAME_MAP[self.game_level]

        # 玩家左边(j - 1)是箱子
        # 且箱子的左边只能是空白或者目的地才可向左
        if map_list[i][j - 1] == BOX_FLAG and (map_list[i][j - 2] == EMPTY_FLAG or map_list[i][j - 2] == DEST_FLAG):
            print('left box')
            map_list[i][j - 1] = PLAYER_FLAG  # 角色向左移动改变角色位置
            self._handle_player_dest()
            map_list[i][j - 2] = BOX_FLAG  # 把箱子向左移改变位置

        # 玩家左边(j - 1)是空白
        elif map_list[i][j - 1] == EMPTY_FLAG:
            print('left empty')
            map_list[i][j - 1] = PLAYER_FLAG  # 角色向左移动改变角色位置
            self._handle_player_dest()

        elif map_list[i][j - 1] == DEST_FLAG:
            # 玩家左边是目的地
            print('left destination')
            map_list[i][j - 1] = PLAYER_DEST_FLAG  # 让角色和目的地重合

            self._handle_player_dest()

    def move_right(self):
        """
        玩家向右移动处理
        """
        print("move right")

        i, j = self.player_pos
        map_list = GAME_MAP[self.game_level]

        # 玩家右边(j + 1)是箱子
        # 且箱子的右边边只能是空白或者目的地才可向左拖动箱子
        if map_list[i][j + 1] == BOX_FLAG and (map_list[i][j + 2] == EMPTY_FLAG or map_list[i][j + 2] == DEST_FLAG):
            print('right box')
            map_list[i][j + 1] = PLAYER_FLAG  # 角色向左移动改变角色位置
            self._handle_player_dest()
            map_list[i][j + 2] = BOX_FLAG  # 把箱子向左移改变位置

        # 玩家右边(j + 1)是空白
        elif map_list[i][j + 1] == EMPTY_FLAG:
            print('right empty')
            map_list[i][j + 1] = PLAYER_FLAG  # 角色向左移动改变角色位置
            self._handle_player_dest()

        elif map_list[i][j + 1] == DEST_FLAG:
            # 玩家优边是目的地
            print('right destination')
            map_list[i][j + 1] = PLAYER_DEST_FLAG  # 让角色和目的地重合

            self._handle_player_dest()

    def _player_move_event_handle(self, direction: MoveDirection):
        """
        玩家上下左右移动事件处理
        Args:
            direction: 移动的方向

        """

        # 记录上下左右待判断的位置
        # i,j 玩家原来位置 上下 m，k  左右 n，v
        i, j = self.player_pos
        m, n = self.player_pos
        k, v = self.player_pos
        map_list = GAME_MAP[self.game_level]

        # 根据不同的移动方向确定判定条件
        if direction == MoveDirection.UP:  # 向上 (i - 1, j)、(i - 2, j)
            m = i - 1
            k = i - 2
        elif direction == MoveDirection.DOWN:  # 向下 (i + 1, j)、(i + 2, j)
            m = i + 1
            k = i + 2
        elif direction == MoveDirection.LEFT:  # 向左 (i, j - 1)、(i, j - 2)
            n = j - 1
            v = j - 2
        elif direction == MoveDirection.RIGHT:  # 向右 (i, j + 1)、(i, j + 2)
            n = j + 1
            v = j + 2

        def handle_player_dest_coincide():
            """
            角色和目的地重合判断处理
            """
            if map_list[i][j] == PLAYER_DEST_FLAG:
                map_list[i][j] = DEST_FLAG  # 是，把原来角色位置改成目的地
            else:
                map_list[i][j] = EMPTY_FLAG  # 不是，把原来角色位置改成空白

        # 玩家(上下左右)边是箱子或者箱子和目的地重合
        # 且箱子的(上下左右)边只能是空白或者目的地才可向上
        if map_list[m][n] in [BOX_FLAG, BOX_DEST_FLAG] and \
                map_list[k][v] in [EMPTY_FLAG, DEST_FLAG]:

            if map_list[m][n] == BOX_DEST_FLAG:  # 如果移动的位置是箱子与目的地的重合
                map_list[m][n] = PLAYER_DEST_FLAG  # 让角色和目的地重合
            else:
                map_list[m][n] = PLAYER_FLAG  # 角色向上移动改变角色位置

            # 判断当前位置是否是角色和目的地重合
            handle_player_dest_coincide()

            # 判断箱子是否与目的地重合
            if map_list[k][v] == DEST_FLAG:
                map_list[k][v] = BOX_DEST_FLAG  # 标记箱子和目的地重合
            else:
                map_list[k][v] = BOX_FLAG  # 把箱子向上移改变位置

        elif map_list[m][n] == EMPTY_FLAG:  # 判断(上下左右)边是否空白

            map_list[m][n] = PLAYER_FLAG  # 角色向上移动改变角色位置

            # 判断当前位置是否是角色和目的地重合
            handle_player_dest_coincide()

        elif map_list[m][n] == DEST_FLAG:  # 判断(上下左右)边是否是目的地

            map_list[m][n] = PLAYER_DEST_FLAG  # 让角色和目的地重合

            # 判断当前位置是否是角色和目的地重合
            handle_player_dest_coincide()

    def _event_handle(self):
        """事件处理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                # 玩家向左移动
                self._player_move_event_handle(direction=MoveDirection.LEFT)
                # self.move_lef()

            elif key_pressed[K_d] or key_pressed[K_RIGHT]:
                # 玩家向右移动
                self._player_move_event_handle(direction=MoveDirection.RIGHT)
                # self.move_right()

            elif key_pressed[K_w] or key_pressed[K_UP]:
                # 玩家向上移动
                self._player_move_event_handle(direction=MoveDirection.UP)
                # self.move_up()

            elif key_pressed[K_s] or key_pressed[K_DOWN]:
                # 玩家上下移动
                self._player_move_event_handle(direction=MoveDirection.DOWN)
                # self.move_down()

    def run_game(self):

        # 主循环事件监听与渲染
        while True:
            # 设置游戏刷新帧率
            pygame.time.Clock().tick(self.game_fps)

            # 绘制地图
            self.game_screen.blit(source=self.bg_screen, dest=(0, 0))
            self.draw_map()

            # 事件处理
            self._event_handle()

            pygame.display.flip()


def main():
    RabbitBox().run_game()


if __name__ == '__main__':
    main()
