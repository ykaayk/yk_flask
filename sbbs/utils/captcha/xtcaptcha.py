# coding:utf8

import random
import string
# pip insatll Pillow
# Image:是一个画板(context),ImageDraw:是一个画笔, ImageFont:画笔的字体
from PIL import Image, ImageDraw, ImageFont
from utils import xtcache


# Captcha验证码
class Captcha(object):
    # 把一些常量抽取成类属性
    font_path = 'utils/captcha/verdana.ttf'  # 字体路径
    font_size = 25  # 字体大小
    number = 4  # 验证码的位数
    bg_color = (255, 255, 255)  # 背景颜色
    size = (100, 30)  # 验证码图片的尺寸

    # 是否要干扰线
    draw_line = True
    draw_number = 3  # 干扰线数量
    # 是否要干扰点
    draw_point = True

    # 随机字符集合，并剔除容易混淆的字符
    SOURCE = list(string.letters)
    for index in range(0, 10):
        SOURCE.append(str(index))
    for i in 'oOiIlL10sS5':
        SOURCE.remove(i)

    # 随机生成一个字符串
    # 定义成类方法，然后是私有的，对象在外不能直接调用
    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.SOURCE, cls.number))

    # 绘制干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        # 随机干扰线的随机颜色
        line_color = (random.randint(0, 220), random.randint(0, 220), random.randint(0, 220))
        # 随机干扰线的起止点坐标
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=line_color)

    # 绘制干扰点
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(random.randint(0, 220), random.randint(0, 220), random.randint(0, 220)))

    # 生成验证码
    @classmethod
    def gene_code(cls):

        # 随机字体颜色
        font_color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

        width, height = cls.size  # 宽和高
        image = Image.new('RGBA', (width, height), cls.bg_color)  # 创建图片
        font = ImageFont.truetype(cls.font_path, cls.font_size)  # 验证码的字体
        draw = ImageDraw.Draw(image)  # 创建画笔
        text = cls.gene_text()  # 生成字符串
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font, fill=font_color)  # 填充字符串

        # 是否绘制干扰线
        if cls.draw_line:
            for x in xrange(cls.draw_number):
                cls.__gene_line(draw, width, height)
        # 是否绘制噪点
        if cls.draw_point:
            cls.__gene_points(draw, 10, width, height)

        print text  # 验证码

        return text, image

    # 验证验证码
    @classmethod
    def check_captcha(cls, captcha):
        captcha_lower = captcha.lower()
        if xtcache.get(captcha_lower):
            xtcache.delete(captcha_lower)
            return True
        else:
            return False

# # Captcha验证码
# class Captcha(object):
#     # 把一些常量抽取成类属性
#     font_path = 'utils/captcha/swissel.ttf'  # 字体的位置
#     number = 4  # 生成几位数的验证码
#     size = (100, 30)  # 生成验证码图片的宽度和高度
#     bg_color = (255, 255, 255)  # 背景颜色默认为白色 RGB(RE, GREEN, BLUE)
#     font_color = (random.randint(0, 220), random.randint(0, 200), random.randint(0, 200))  # 随机字体的颜色
#     line_color = (random.randint(0, 220), random.randint(0, 220), random.randint(0, 220))  # 随机干扰线颜色
#     font_size = 25  # 验证码字体大小
#     draw_line = True  # 是否加入干扰线
#     draw_point = True  # 是否加入干扰点
#     line_number = 2  # 干扰线条数
#
#     # 去除I/O/o/1/0/L易混淆的字母和数字
#     SOURCE = list(string.letters)
#     for index in range(0, 10):
#         SOURCE.append(str(index))
#     for word in ['I', 'l', '1', 'o', 'O', '0']:
#         SOURCE.remove(word)
#
#     # 定义成类方法，然后是私有的，对象在外不能直接调用
#     # 用来随机生成一个字符串
#     @classmethod
#     def gene_text(cls):
#         return ''.join(random.sample(cls.SOURCE, cls.number))
#
#     # 用来绘制干扰线
#     @classmethod
#     def __gene_line(cls, draw, width, height):
#         begin = (random.randint(0, width), random.randint(0, height))
#         end = (random.randint(0, width), random.randint(0, height))
#         draw.line([begin, end], fill=cls.line_color)
#
#     # 用来绘制干扰点
#     @classmethod
#     def __gene_points(cls, draw, point_chance, width, height):
#         chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
#         for w in xrange(width):
#             for h in xrange(height):
#                 tmp = random.randint(0, 100)
#                 if tmp > 100 - chance:
#                     draw.point((w, h), fill=(0, 0, 0))
#
#     # 生成验证码
#     @classmethod
#     def gene_code(cls):
#         width, height = cls.size  # 宽和高
#         image = Image.new('RGBA', (width, height), cls.bg_color)  # 创建图片
#         font = ImageFont.truetype(cls.font_path, cls.font_size)  # 验证码的字体
#         draw = ImageDraw.Draw(image)  # 创建画笔
#         text = cls.gene_text()  # 生成字符串
#         font_width, font_height = font.getsize(text)
#         draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font, fill=cls.font_color)
#         填充字符串
#         # 如果需要绘制干扰线
#         if cls.draw_line:
#             # 遍历line_number次,就是画line_number根线条
#             for x in xrange(0, cls.line_number):
#                 cls.__gene_line(draw, width, height)
#         # 如果需要绘制噪点
#         if cls.draw_point:
#             cls.__gene_points(draw, 10, width, height)
#
#         return text, image
#
#     @classmethod
#     def check_captcha(cls, captcha):
#         captcha_lower = captcha.lower()
#         if xtcache.get(captcha_lower):
#             xtcache.delete(captcha_lower)
#             return True
#         else:
#             return False


























