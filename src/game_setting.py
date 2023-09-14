#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 游戏配置文件 }
# @Date: 2023/09/13 12:19
import os
from enum import Enum
# from PIL import Image

import pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GRID_SIZE = 90  # 单个方块大小
GAME_TITLE = "🐰兔子吃着月饼🥮上月球🌕"
GAME_ICON = pygame.image.load(os.path.join(BASE_DIR, "res/img/rabbit.ico"))

# 游戏墙素材
WALLS = [
    pygame.image.load(os.path.join(BASE_DIR, "res/img/lantern.png")),
    pygame.image.load(os.path.join(BASE_DIR, "res/img/fireworks.png")),
    pygame.image.load(os.path.join(BASE_DIR, "res/img/fireworks_02.png")),
]

# 游戏角色素材
PLAYERS = [
    pygame.image.load(os.path.join(BASE_DIR, "res/img/rabbit.png")),
    pygame.image.load(os.path.join(BASE_DIR, "res/img/rabbit_01.png")),
]

# 游戏箱子素材
BOXS = [
    *[pygame.image.load(os.path.join(BASE_DIR, "res/img/moon_cake.png"))] * 5,
    pygame.image.load(os.path.join(BASE_DIR, "res/img/donut.png"))
]

# 游戏目的地素材
TERMINAL_BOXS = [
    *[pygame.image.load(os.path.join(BASE_DIR, "res/img/moon_01.png"))] * 3,
    pygame.image.load(os.path.join(BASE_DIR, "res/img/moon_02.png"))
]

# 游戏目的地完成时素材（暂未使用）
FINISHED_BOXS = [
    pygame.image.load(os.path.join(BASE_DIR, "res/img/moon_01.png")),
]

# 游戏背景箱子（暂未使用，直接使用大的背景图）
BG_BOXS = [
    pygame.image.load(os.path.join(BASE_DIR, "res/img/fireworks.png")),
    pygame.image.load(os.path.join(BASE_DIR, "res/img/fireworks_02.png")),
    pygame.image.load(os.path.join(BASE_DIR, "res/img/star.png")),
]

# 游戏背景图
BG_IMAGES = [
    pygame.image.load(os.path.join(BASE_DIR, "res/img/bg_嫦娥_gray.png")),
    *[pygame.image.load(os.path.join(BASE_DIR, "res/img/bg_girl.jpeg"))] * 2,
    *[pygame.image.load(os.path.join(BASE_DIR, "res/img/bg_blue.png"))] * 10,
]


class MoveDirection(Enum):
    """移动方向枚举"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


def main():
    img = Image.open(os.path.join(BASE_DIR, "res/img/bg_fireworks.png")).convert('L')
    img.save('bg_fireworks_gray.png')


if __name__ == '__main__':
    main()
