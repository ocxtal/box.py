#!/usr/bin/python
# -*- coding:utf-8 -*-

# box generator
# usage: python box.py <width> <height> <depth> <thickness> <pitch> <output filename>

from dxfwrite import DXFEngine as dxf
from math import floor
from sys import argv

if len(argv) != 7:
	print("Invalid number of arguments")
	print("usage: ./box.py <width> <height> <depth> <thickness> <pitch> <output filename (.dxf)>")

# 引数のとりだし
w = float(argv[1])		# width
h = float(argv[2])		# height
d = float(argv[3])		# depth
t = float(argv[4])		# thickness
p = float(argv[5])		# pitch
filename = argv[6]

# print w, h, d, t, p

# 箱のピッチの計算
pw = w / floor(w/p)		# 引数で与えられたpitchより少し大きい値で、widthを割り切れる値を計算する
ph = h / floor(h/p)
pd = d / floor(d/p)

#print pw, ph, pd

def generate(width, wpitch, wpol, height, hpitch, hpol):
	h = height
	ph = hpitch
	w = width
	pw = wpitch

	a0 = [[((hpol+1)%2) * t, ((wpol+1)%2) * t]]
	for i in range(int(w/pw)-1):
		a0 += [[(i+1) * pw, ((i+wpol)%2) * t]]
	for i in range(int(h/ph)-1):
		a0 += [[w - ((i+hpol)%2) * t, (i+1) * ph]]
	a0 += [[w - ((int(h/ph)+1+hpol)%2) * t, h - ((int(w/pw)+1+wpol)%2) * t]]

	a1 = [[((hpol+1)%2) * t, ((wpol+1)%2) * t]]
	for i in range(int(h/ph)-1):
		a1 += [[((i+hpol)%2) * t, (i+1) * ph]]
	for i in range(int(w/pw)-1):
		a1 += [[(i+1) * pw, h - ((i+wpol)%2) * t]]
	a1 += [[w - ((int(h/ph)+1+hpol)%2) * t, h - ((int(w/pw)+1+wpol)%2) * t]]

	return([a0, a1])
# end of generate

def plot(drawing, a, offset):
	a0 = a[0]
	a1 = a[1]
	prev_point = [a0[0][0]+offset[0], a0[0][1]+offset[1]]
	for elem in a0:
		point = [elem[0]+offset[0], elem[1]+offset[1]]
		drawing.add(dxf.line(prev_point, [point[0], prev_point[1]], color=7))
		drawing.add(dxf.line([point[0], prev_point[1]], point, color=7))
		prev_point = point

	prev_point = [a1[0][0]+offset[0], a1[0][1]+offset[1]]
	for elem in a1:
		point = [elem[0]+offset[0], elem[1]+offset[1]]
		drawing.add(dxf.line(prev_point, [prev_point[0], point[1]], color=7))
		drawing.add(dxf.line([prev_point[0], point[1]], point, color=7))
		prev_point = point
# end of generate


a = generate(w, pw, 1, d, pd, 1)
b = generate(w, pw, 0, h, ph, 1)
c = generate(h, ph, 0, d, pd, 0)
ai = generate(w, pw, 0, d, pd, 0)
bi = generate(w, pw, 1, h, ph, 0)
ci = generate(h, ph, 1, d, pd, 1)

# dxfファイルの作成
drawing = dxf.drawing(filename)
plot(drawing, a, [0,0]);
plot(drawing, b, [0, d+p])
plot(drawing, c, [w+p, 0])
plot(drawing, ai, [w+h+2*p, 0])
plot(drawing, bi, [w+h+2*p, d+p])
plot(drawing, ci, [2*w+h+3*p, 0])
drawing.save()
#drawing.close()
