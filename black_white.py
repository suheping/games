
# -*- encoding: utf-8 -*-
'''
@File    :   black_white.py
@Time    :   2020/06/19 16:12:09
@Author  :   peace_su
@Version :   1.0
@Contact :   peace_su@163.com
@WebSite :   https://me.csdn.net/u010098760
'''

# here put the import lib


from sys import exit
from pygame.locals import *
import pygame
import random
import copy


# ===========================  初始化数据 begin =====================
# 固定窗口大小：1200*600
SCREEN_SIZE = (1200, 600)

# 步数计数
count = 0

# 字体颜色
font_color = (0, 0, 0)
# 按钮颜色
button_color = (0, 125, 255)
# 答题结束标识
is_over = False
# 隐藏标识
is_hide = False


# 难度level，几乘几
level = 4


def init_grid(level):
    '''
        初始化方格数据，默认 简单 模式
        初始化方格数据，全为False，对应页面为白色
    '''
    grid = [[False for i in range(level)] for j in range(level)]
    return grid


empty_grid = init_grid(level)
# 需要使用深拷贝，不然修改current_grid的值后empty_grid也会修改
current_grid = copy.deepcopy(empty_grid)
# ========================  初始化数据 end =========================


def click_block(x, y, current_grid, level):
    '''
      点击方块方法
    '''
    if isinstance(x, int) and isinstance(y, int):
        if x > level-1 or y > level-1 or x < 0 or y < 0:
            return current_grid
        else:
            # 自己先取反
            current_grid[x][y] = not current_grid[x][y]
            # 判断上测方块是否变化
            if x > 0:
                current_grid[x-1][y] = not current_grid[x-1][y]
            # 判断下测方块是否变化
            if x < level-1:

                current_grid[x+1][y] = not current_grid[x+1][y]
            # 判断左侧方块是否变化
            if y > 0:
                current_grid[x][y-1] = not current_grid[x][y-1]
            # 判断右侧方块是否变化
            if y < level-1:
                current_grid[x][y+1] = not current_grid[x][y+1]
            return current_grid
    else:
        return current_grid


def generate_topic(level):
    '''
        生成题目方法
    '''
    tmp = [True, False]
    t = []
    for i in range(level):
        t1 = []
        for j in range(level):
            t1.append(random.choice(tmp))
        t.append(t1)
    return t


# 生成题目
topic = generate_topic(level)


# 初始化pygame
pygame.init()

# 创建一个窗口，40*480大小的，0-基本就选这个了，32-代表颜色深度8-32
screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
# 定义窗口title
pygame.display.set_caption("黑白消融")


def draw_block(init_x, init_y, level):
    '''
        画x乘x的格子
        将高度的3/4，宽度的3/8填充满x乘x的格子，格子之间空两个像素
        一个格子 宽高均为 (高度的3/4/level)-2
    '''
    width = (SCREEN_SIZE[0]*3/8/level)-2
    height = (SCREEN_SIZE[1]*3/4/level)-2
    rs = []
    for i in range(level):
        tmp = []
        for j in range(level):
            tmp.append(Rect(
                init_x+j*(SCREEN_SIZE[0]*3/8/level), init_y+i*(SCREEN_SIZE[1]*3/4/level), width, height))
        rs.append(tmp)
    return rs


def write(msg="Winning!!!", color=(255, 255, 0), height=14):
    '''
        写字到屏幕上
    '''
    myfont = pygame.font.Font('C:/Windows/Fonts/simsun.ttc', height)
    # myfont = pygame.font.SysFont("arial", height)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext


def init_screen(current_grid):
    '''
        画屏幕
    '''
    # 设置背景色，白色
    screen.fill((255, 255, 255))
    # 画左侧窗口：题目区
    pygame.draw.rect(screen, (125, 125, 125),
                     (0, 0, SCREEN_SIZE[0]/2-2, SCREEN_SIZE[1]))
    # 画右侧窗口：答题区
    pygame.draw.rect(screen, (125, 125, 125), (SCREEN_SIZE[0]/2+2, 0,
                                               SCREEN_SIZE[0]/2-2, SCREEN_SIZE[1]))
    if is_hide:
        pygame.draw.rect(screen, (0, 0, 255), (SCREEN_SIZE[0]/16, SCREEN_SIZE[1]/8,
                                               SCREEN_SIZE[0]*3/8, SCREEN_SIZE[1]*3/4))
        screen.blit(write("不要偷看哦~", height=int(SCREEN_SIZE[1]/8),
                          color=font_color), (SCREEN_SIZE[0]*3/40, SCREEN_SIZE[1]*7/20))
    else:
        # 画题目区方格，颜色
        # 左上角格子坐标是(100,100)
        ts = draw_block(SCREEN_SIZE[0]/16, SCREEN_SIZE[1]/8, level)
        for i in range(len(ts)):
            for j in range(len(ts[i])):
                if topic[i][j]:
                    block_color = (1, 1, 1)
                else:
                    block_color = (255, 255, 255)
                pygame.draw.rect(screen, block_color, ts[i][j])

    # 画答题区方格，颜色按照current_grid显示
    # 左上角格子坐标是(900,100)
    rs = draw_block(SCREEN_SIZE[0]*9/16, SCREEN_SIZE[1]/8, level)
    for i in range(len(rs)):
        for j in range(len(rs[i])):
            if current_grid[i][j]:
                block_color = (1, 1, 1)
            else:
                block_color = (255, 255, 255)
            pygame.draw.rect(screen, block_color, rs[i][j])

    # 把“题目”放在屏幕上
    screen.blit(
        write("题目", height=int(SCREEN_SIZE[1]/16), color=font_color), (SCREEN_SIZE[0]*7/32, SCREEN_SIZE[1]/40))
    # 把“答题区”放在屏幕上
    screen.blit(
        write("答题区", height=int(SCREEN_SIZE[1]/16), color=font_color), (SCREEN_SIZE[0]*23/32, SCREEN_SIZE[1]/40))
    # 把“步数”放在屏幕上
    screen.blit(
        write("步数：", height=int(SCREEN_SIZE[1]/40), color=font_color), (SCREEN_SIZE[0]*27/32, SCREEN_SIZE[1]*7/80))
    # 把count值放在屏幕上
    screen.blit(write(str(count), height=int(SCREEN_SIZE[1]/40),
                      color=font_color), (SCREEN_SIZE[0]*141/160, SCREEN_SIZE[1]*7/80))

    # 换题按钮
    pygame.draw.rect(screen, button_color,
                     (SCREEN_SIZE[0]/8, SCREEN_SIZE[1]*9/10, SCREEN_SIZE[0]*3/32, SCREEN_SIZE[1]*3/40))
    screen.blit(write("换题", height=int(SCREEN_SIZE[1]/20),
                      color=font_color), (SCREEN_SIZE[0]*23/160, SCREEN_SIZE[1]*73/80))
    # 遮挡按钮
    pygame.draw.rect(screen, button_color, (SCREEN_SIZE[0]*9/32,
                                            SCREEN_SIZE[1]*9/10, SCREEN_SIZE[0]*3/32, SCREEN_SIZE[1]*3/40))
    screen.blit(write("遮挡", height=int(SCREEN_SIZE[1]/20),
                      color=font_color), (SCREEN_SIZE[0]*3/10, SCREEN_SIZE[1]*73/80))
    # 重置按钮
    pygame.draw.rect(screen, button_color, (
        SCREEN_SIZE[0]*5/8, SCREEN_SIZE[1]*9/10, SCREEN_SIZE[0]*3/32, SCREEN_SIZE[1]*3/40))
    screen.blit(write("重置", height=int(SCREEN_SIZE[1]/20),
                      color=font_color), (SCREEN_SIZE[0]*103/160, SCREEN_SIZE[1]*73/80))
    # 提交按钮
    pygame.draw.rect(screen, button_color,
                     (SCREEN_SIZE[0]*25/32, SCREEN_SIZE[1]*9/10, SCREEN_SIZE[0]*3/32, SCREEN_SIZE[1]*3/40))
    screen.blit(write("提交", height=int(SCREEN_SIZE[1]/20),
                      color=font_color), (SCREEN_SIZE[0]*4/5, SCREEN_SIZE[1]*73/80))
    # 将修改难度的提示显示在窗口右下角
    screen.blit(write("点击2~10修改题目难度", height=int(
        SCREEN_SIZE[1]/40), color=font_color), (SCREEN_SIZE[0]-11*(SCREEN_SIZE[1]/40), SCREEN_SIZE[1]-SCREEN_SIZE[1]/40))


while True:

    if not is_over:
        init_screen(current_grid)

    for event in pygame.event.get():
        # 点窗口的X退出
        if event.type == QUIT:
            exit()
        # 更改窗口大小
        elif event.type == VIDEORESIZE:
            SCREEN_SIZE = event.dict['size']
            screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
        elif event.type == KEYDOWN:
            # 变更难度
            if event.key == K_2:
                level = 2
                topic = generate_topic(level)
                empty_grid = init_grid(level)
                current_grid = copy.deepcopy(empty_grid)
                count = 0
            elif event.key == K_3:
                level = 3
                topic = generate_topic(level)
                empty_grid = init_grid(level)
                current_grid = copy.deepcopy(empty_grid)
                count = 0
            elif event.key == K_4:
                level = 4
                topic = generate_topic(level)
                empty_grid = init_grid(level)
                current_grid = copy.deepcopy(empty_grid)
            elif event.key == K_5:
                level = 5
                topic = generate_topic(level)
                empty_grid = init_grid(level)
                current_grid = copy.deepcopy(empty_grid)
            elif event.key == K_6:
                level = 6
                topic = generate_topic(level)
                empty_grid = init_grid(level)
                current_grid = copy.deepcopy(empty_grid)
            elif event.key == K_7:
                level = 7
                topic = generate_topic(level)
                empty_grid = init_grid(level)
                current_grid = copy.deepcopy(empty_grid)
            elif event.key == K_8:
                level = 8
                topic = generate_topic(level)
                empty_grid = init_grid(level)
                current_grid = copy.deepcopy(empty_grid)
            elif event.key == K_9:
                level = 9
                topic = generate_topic(level)
                empty_grid = init_grid(level)
                current_grid = copy.deepcopy(empty_grid)
            elif event.key == K_0:
                level = 10
                topic = generate_topic(level)
                empty_grid = init_grid(level)
                current_grid = copy.deepcopy(empty_grid)
        elif event.type == MOUSEBUTTONDOWN:
            # 如果点击了鼠标左键，取到当前鼠标的坐标
            pressed_array = pygame.mouse.get_pressed()
            if pressed_array[0] == 1:
                is_over = False
                mouse_x, mouse_y = event.pos
                # 判断是否点击了答题区格子范围
                if mouse_x >= SCREEN_SIZE[0]*9/16 and mouse_x <= SCREEN_SIZE[0]*15/16 and mouse_y >= SCREEN_SIZE[1]/8 and mouse_y <= SCREEN_SIZE[1]*7/8:
                    # 调click_block方法
                    click_block(int((mouse_y-SCREEN_SIZE[1]/8) // int(SCREEN_SIZE[1]*3/4/level)), int((
                        mouse_x-SCREEN_SIZE[0]*9/16) // int(SCREEN_SIZE[1]*3/4/level)), current_grid, level)
                    # 点击有效，步数+1
                    count = count + 1
                # 如果点击了换题按钮
                elif mouse_x >= SCREEN_SIZE[0]/8 and mouse_x <= SCREEN_SIZE[0]*7/32 and mouse_y >= SCREEN_SIZE[1]*9/10 and mouse_y <= SCREEN_SIZE[1]*39/40:
                    # 换题
                    new_topic = generate_topic(level)
                    topic = new_topic
                    # 去掉遮挡
                    is_hide = False
                    # 答题区重置
                    empty_grid = init_grid(level)
                    current_grid = copy.deepcopy(empty_grid)
                    count = 0
                # 如果点击了提交按钮
                elif mouse_x >= SCREEN_SIZE[0]*25/32 and mouse_x <= SCREEN_SIZE[0]*7/8 and mouse_y >= SCREEN_SIZE[1]*9/10 and mouse_y <= SCREEN_SIZE[1]*39/40:
                    is_over = True
                    if current_grid == topic:
                        screen.blit(write("VICTORY !!!", height=int(SCREEN_SIZE[1]/4),
                                          color=(255, 255, 0)), (SCREEN_SIZE[0]/4, SCREEN_SIZE[1]*3/8))
                    else:
                        screen.blit(write("DEFEAT !!!", height=int(SCREEN_SIZE[1]/4),
                                          color=(255, 0, 0)), (SCREEN_SIZE[0]/4, SCREEN_SIZE[1]*3/8))
                    # 提示用户点击任意位置继续
                    screen.blit(write("鼠标点击任意位置继续~", height=int(SCREEN_SIZE[1]/16),
                                      color=button_color), (SCREEN_SIZE[0]*3/8, SCREEN_SIZE[1]*3/4))
                # 如果点击了遮挡按钮
                elif mouse_x >= SCREEN_SIZE[0]*9/32 and mouse_x <= SCREEN_SIZE[0]*3/8 and mouse_y >= SCREEN_SIZE[1]*7/8 and mouse_y <= SCREEN_SIZE[1]*39/40:
                    is_hide = not is_hide
                # 如果点击了重置按钮
                elif mouse_x >= SCREEN_SIZE[0]*5/8 and mouse_x <= SCREEN_SIZE[0]*23/32 and mouse_y >= SCREEN_SIZE[1]*7/8 and mouse_y <= SCREEN_SIZE[1]*39/40:
                    count = 0
                    current_grid = copy.deepcopy(init_grid(level))

        # 刷新窗口
        pygame.display.update()
