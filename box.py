#!/usr/bin/env python
# -*- coding:utf-8 -*-

# box generator
# usage: python box.py <width> <height> <depth> <thickness> <pitch> <output filename>

from dxfwrite import DXFEngine as dxf
from math import floor

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

if __name__ == '__main__':
	import sys
	from optparse import OptionParser
	p = OptionParser(usage = "python box.py <width> <height> <depth> > out.dxf # all dimensions are in millimeters")
	p.add_option("-t", "--thickness", dest = "t", help = "board thickness (in millimeters)", default = 5)
	p.add_option("-p", "--pitch", dest = "p", help = "cog pitch (in millimeters)", default = 10)
	p.add_option("-o", "--output", dest = "o", help = "output file name")

	(opt, args) = p.parse_args()

	if len(args) == 0:
		p.error("at least one dimension (width) must be given as positional argument.")
	elif len(args) < 3:
		args.append(args[0])
		args.append(args[0])

	w = float(args[0])		# width
	h = float(args[1])		# height
	d = float(args[2])		# depth
	t = float(opt.t)		# thickness
	p = float(opt.p)		# pitch
	filename = opt.o
	# print w, h, d, t, p
	# calc pitch
	pw = w / floor(w/p)
	ph = h / floor(h/p)
	pd = d / floor(d/p)

	#print pw, ph, pd

	a = generate(w, pw, 1, d, pd, 1)
	b = generate(w, pw, 0, h, ph, 1)
	c = generate(h, ph, 0, d, pd, 0)
	ai = generate(w, pw, 0, d, pd, 0)
	bi = generate(w, pw, 1, h, ph, 0)
	ci = generate(h, ph, 1, d, pd, 1)

	# dxfファイルの作成
	drawing = dxf.drawing()
	plot(drawing, a, [0,0]);
	plot(drawing, b, [0, d+p])
	plot(drawing, c, [w+p, 0])
	plot(drawing, ai, [w+h+2*p, 0])
	plot(drawing, bi, [w+h+2*p, d+p])
	plot(drawing, ci, [2*w+h+3*p, 0])
	drawing.save_to_fileobj(open(opt.o, "w") if opt.o is not None else sys.stdout)
	#drawing.close()
