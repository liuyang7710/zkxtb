#!/usr/bin/env python3.6.5
# -*- coding: utf-8 -*-

__author__ = 'peng zhao'

import os
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class cfg:
    base_path = "E:/舰船数据/DOTA/"
    mode = "val"
    img_path = os.path.join(base_path, "origin", mode, "images")
    txt_path = os.path.join(base_path, "origin", mode, "labelTxt-v1.0", "labelTxt")
    vis_path = os.path.join(base_path, "vis", mode)


def vis_img():
    total = len(os.listdir(cfg.img_path))
    for index, img_name in enumerate(os.listdir(cfg.img_path)):
        if img_name.endswith('.png'):
            try:
                im = Image.open(os.path.join(cfg.img_path, img_name))
                draw = ImageDraw.Draw(im)
                font = ImageFont.truetype("./fonts/simhei.ttf", 14, encoding="utf-8")

                with open(os.path.join(cfg.txt_path, img_name.replace('.png', '.txt')), 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                for line in lines[2:]:
                    x1, y1, x2, y2, x3, y3, x4, y4, category, difficult = line.split(' ')
                    draw.polygon([(int(x1), int(y1)), (int(x2), int(y2)), (int(x3), int(y3)), (int(x4), int(y4))], outline=(255, 0, 0))
                    draw.text((int(x1), int(y1) - 20), "{0}".format(category), (0, 0, 255), font=font)
                im.save(os.path.join(cfg.vis_path, img_name))
                print("第{0}/{1}张图片可视化完成：{2}".format(index + 1, total, img_name))
            except Exception as e:
                print("===>第{0}/{1}张图片出错：{2}".format(index + 1, total, img_name))
                continue


if __name__ == '__main__':
    vis_img()
