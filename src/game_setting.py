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

# 游戏背景音乐
BG_MUSICS = [
    os.path.join(BASE_DIR, "res/music/卡农.mp3"),
    os.path.join(BASE_DIR, "res/music/龙珠.mp3"),
]
# 游戏音乐结束事件
MUSIC_END_EVENT = pygame.USEREVENT + 6

# 游戏音乐音量
MUSIC_VOLUME = 5

# 历史地图最大保留最近10步
HISTORY_MAP_MAX_CAP = 10

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

# 中秋古诗词
ANCIENT_POEMS = [
    "❤️但愿人长久，千里共婵娟🎆",
    "🏮今夜月明人尽望，不知秋思落谁家🏮",
    "🌟明月几时有？ 把酒问青天🌟",
    "🥮万里无云镜九州，最团圆夜是中秋🥮",
    "🌕三五夜中新月色, 二千里外故人心🌕",
    "🌕嫦娥应悔偷灵药, 碧海青天夜夜心🌕",
    "🥮此生此夜不长好, 明月明年何处看?🥮",
    "🌟此夜中秋月，清光十万家🌟",
    "🏮若得长圆如此夜，人情未必看承别🏮",
    "❤️明月易低人易散, 归来呼酒更重看🎆",
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
