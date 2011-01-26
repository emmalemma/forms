from PIL import Image, ImageDraw
from pytesser import *

import couchdb

im = Image.open("tiffs/MA_moped.tiff")
#im.show()

api_key = "parenignodscuryouldrerve"
password = "xxSpEupF4O8DfL4r1y5tvBVT"

pixmap = {}
groupmap = {}
groupct = 0
bounds = {}
fields = []

width, height = im.size

def white(val):
	return len([v for v in val if v > 250]) 

def adjacent_pixels(xy):
	pix = []
	x,y = xy
	if x > 0:
		pix.append((x-1,y))
		if y > 0:
			pix.append((x-1,y-1))
	if y > 0:
		pix.append((x,y-1))
		if x < width-1:
			pix.append((x+1, y-1))
	return pix

def double_adjacent(xy):
	pix = []
	for p in adjacent_pixels(xy):
		pix.append(p)
		pix += adjacent_pixels(p)
	return pix

def map_groups(groups):
	#print groups
	for i in range(1,len(groups)):
		if groups[i] != groups[i-1]:
			#print "mapping",groups[i],"to",groups[i-1]
			groupmap[groups[i]] = groups[i-1]
		
def group_of(xy):
	x,y = xy
	try:
		return pixmap[y][x]
	except KeyError:
		return None

def set_group(xy, group):
	x, y = xy
	if pixmap.has_key(y):
		pixmap[y][x] = group
	else:
		pixmap[y] = {x: group}

def new_group():
	global groupct
	groupct += 1
	return groupct

def rebound(xy, group):
	x, y = xy
	if bounds.has_key(group):
		bound = bounds[group]
		if x < bound[0]:
			bound[0] = x	
		elif x > bound[2]:
			bound[2] = x
			
		if y < bound[1]:
			bound[1] = y
		elif y > bound[3]:
			bound[3] = y
	else:
		bounds[group] = [x,y,x,y]

def find_label(field):
	x1,y1,x2,y2 = field
	scan = []
	for k in bounds:
		rect = bounds[k]
		rx1,ry1,rx2,ry2 = rect
		if rx2 < x2 and y1 - ry1 < 40 and ry2 - y2 < 40:
			scan.append(rect)
	scan.sort(key=lambda x: -x[0])
	label = scan[0]
	
	if label[2] > x1:
		return None 
		
	oldleft = label[0]
	for rect in scan:
		x1,y1,x2,y2 = rect
		
		#print "x1:", x1, "oldleft:",oldleft,"x1-oldleft:", x1-oldleft
		if oldleft - x1 > 50:
			break
		oldleft = x1
		
		if x1 < label[0]:
			label[0] = x1
		if x2 > label[2]:
			label[2] = x
		if y1 < label[1]:
			label[1] = y1
		if y2 > label[3]:
			label[3] = y2
	return label

print im.size[1]

print "mapping groups..."
for y in range(height):
	if not y % 100:
		print y, groupct
	for x in range(width):
		pixel = im.getpixel((x, y))
		if not white(pixel):
			groups = [group for group in [group_of(adjacent) for adjacent in adjacent_pixels((x, y))] if group]
			groups.sort()
			set_group((x,y), groups[0] if len(groups) else new_group())
			map_groups(groups)

print "remapping groups..."
print len(pixmap.keys())
for y in pixmap.keys():
	if not y % 100:
		print y
	for x in pixmap[y].keys():
		group = pixmap[y][x]
		try:
			while True:
				if group == groupmap[group]:
					break
				group = groupmap[group]
		except KeyError:
			pass
		pixmap[y][x] = group
		rebound((x,y), group)

#print bounds
dpi = im.info['dpi'][0]
def pixels_to_points(px):
	return px * 72/dpi
p2p = pixels_to_points

draw = ImageDraw.Draw(im)
proof = im.copy()
for k in bounds:
	rect = bounds[k]
	x,y,x2,y2 = rect
	w,h = x2-x, y2-y
	draw.rectangle(rect, outline = '#F00')
	#draw.text(rect[:2],str(k), fill = '#0F0')
	if h != 0 and w/h > 10:
		#draw.text(rect[:2], "field?", fill = '#0F0')
		label = find_label(rect)
		if label and label[2] - label[0] > 0:
			draw.rectangle(label, outline = '#00F')
			crop = proof.crop(label)
			text = image_to_string(crop).strip()
			if text:
				print "identified field", text
				draw.text(rect[:2], text, fill = '#0F0' )
				fields.append({'field': "text", 'label': text, 'output': {'x': p2p(x), 'y': p2p(y), 'w': p2p(w), 'h': p2p(20)}})

del draw
im.show()

print fields

couch = couchdb.Server('http://localhost:5984/')
db = couch['forms']



#print allgroups

			

	
