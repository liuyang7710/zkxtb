#!/usr/bin/env python3.6.5
# -*- coding: utf-8 -*-

__author__ = 'peng zhao'

import os
from PIL import Image, ImageDraw, ImageFont
import xml.dom.minidom as xml_dom


class cfg:
    base_path = "E:/舰船数据/Ships/"
    xml_path = os.path.join(base_path, "xml")
    tif_path = os.path.join(base_path, "tif")
    txt_path = os.path.join(base_path, "txt")
    vis_path = os.path.join(base_path, "vis")


def data_transform():
    for xml_name in os.listdir(cfg.xml_path):
        if xml_name.endswith('.xml'):
            txt_file = open(os.path.join(cfg.txt_path, xml_name.replace('.xml', '.txt')), 'w', encoding='utf-8')
            # 得到文档对象
            dom_obj = xml_dom.parse(os.path.join(cfg.xml_path, xml_name))
            # 得到元素对象
            element_obj = dom_obj.documentElement
            # 获得子标签
            objects = element_obj.getElementsByTagName("Object")
            pixels = element_obj.getElementsByTagName("Pixel")
            for i in range(len(objects)):
                # 获得标签对之间的数据
                category = objects[i].firstChild.data
                coords = {}
                pts = pixels[i].getElementsByTagName("Pt")
                for p in pts:
                    coords[str(p.getAttribute("index"))] = {}
                    coords[str(p.getAttribute("index"))]["x"] = int(float(str(p.getAttribute("LeftTopX"))))
                    coords[str(p.getAttribute("index"))]["y"] = int(float(str(p.getAttribute("LeftTopY"))))
                print(category, coords)
                txt_file.write("{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(coords['4']['x'], coords['4']['y'],
                                                                            coords['3']['x'], coords['3']['y'],
                                                                            coords['2']['x'], coords['2']['y'],
                                                                            coords['1']['x'], coords['1']['y'],
                                                                            category))
            txt_file.close()


def vis_img():
    for tif_name in os.listdir(cfg.tif_path):
        if tif_name.endswith('.tif'):
            im = Image.open(os.path.join(cfg.tif_path, tif_name))
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype("./fonts/simhei.ttf", 16, encoding="utf-8")

            with open(os.path.join(cfg.txt_path, tif_name.replace('.tif', '.txt')), 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                x1, y1, x2, y2, x3, y3, x4, y4, category = line.split(',')
                draw.polygon([(int(x1), int(y1)), (int(x2), int(y2)), (int(x3), int(y3)), (int(x4), int(y4))], outline=(255, 0, 0))
                draw.text((int(x1), int(y1) - 20), "{0}".format(category), (0, 0, 255), font=font)
            im.save(os.path.join(cfg.vis_path, tif_name))


if __name__ == '__main__':
    data_transform()
    vis_img()
