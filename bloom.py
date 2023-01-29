import pygame, math
import sys
pygame.init()

SCREEN_WIDTH=500
SCREEN_HEIGHT=500
FPS=24

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bloom")
clock=pygame.time.Clock()

image_path="cherryblossom.jpg"
image=pygame.image.load(image_path)

SCREEN_WIDTH=image.get_width()
SCREEN_HEIGHT=image.get_height()
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

slider_percent=0.5
e=2.71828
steepness_percent=0.1 #0 to 100

def binary_threshold(img):
	res=pygame.Surface((img.get_width(), img.get_height()))
	steepness=-(steepness_percent*100)
	sp=(1-slider_percent)
	for x in range(img.get_width()):
		for y in range(img.get_height()):
			inp=img.get_at((x,y))
			g=(inp[0]+inp[1]+inp[2])/3/255
			r=1/(1+(math.pow(e, steepness*(g-sp))))
			r*=255
			res.set_at((x,y), (r,r,r))
	return res
def average_colour(c1,c2):
	return ((c1[0]+c2[0])/2,(c1[1]+c2[1])/2,(c1[2]+c2[2])/2)
SCALE_FACTOR=0.5
BLUR_ITER=5
def box_blur(img,):
	# org_size=img.get_size()
	# res=pygame.transform.scale(img, (img.get_width()*SCALE_FACTOR, img.get_height()*SCALE_FACTOR))
	res=img.copy()
	for _ in range(BLUR_ITER):
		for y in range(res.get_height()):
			for x in range(1,res.get_width()-1):
				a1=res.get_at((x-1,y))
				a2=res.get_at((x+1,y))
				res.set_at((x,y), average_colour(a1,a2))
		for x in range(res.get_width()):
			for y in range(1,res.get_height()-1):
				a1=res.get_at((x,y-1))
				a2=res.get_at((x,y+1))
				res.set_at((x,y), average_colour(a1,a2))
	# return pygame.transform.scale(res, org_size)
	return res

original_size=image.get_size()

def bloom(img):
	res_image=img.copy()
	res_image.blit(box_blur(binary_threshold(img)), (0,0), special_flags=pygame.BLEND_RGB_ADD)
	return pygame.transform.scale(res_image, original_size)

img_scaled=pygame.transform.scale(image, (image.get_width()*SCALE_FACTOR, image.get_height()*SCALE_FACTOR))
res_image=bloom(img_scaled)


slider_rect=pygame.Rect((10, SCREEN_HEIGHT-10-5, SCREEN_WIDTH-10-10-10, 10))
sliding=False

slider2_rect=pygame.Rect((5, 10, 10, SCREEN_HEIGHT-10-10-10))
sliding2=False
while 1:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mpos=pygame.mouse.get_pos()
			slider_x=slider_rect.left+slider_rect.width*slider_percent
			if math.dist(mpos, (slider_x, slider_rect.centery)) < 10:
				sliding=True
			elif math.dist(mpos, (slider2_rect.centerx, slider2_y)) < 10:
				sliding2=True
		elif event.type == pygame.MOUSEBUTTONUP:
			sliding=False
			sliding2=False
			res_image=bloom(img_scaled)

	if sliding:
		mpos=pygame.mouse.get_pos()
		lx=(mpos[0]-10)/slider_rect.width
		if lx > 1: lx=1
		if lx < 0: lx=0
		slider_percent=lx
	if sliding2:
		mpos=pygame.mouse.get_pos()
		lx=(mpos[1]-10)/slider2_rect.height
		if lx > 1: lx=1
		if lx < 0: lx=0
		steepness_percent=lx

	screen.blit(res_image, (0,0))

	pygame.draw.rect(screen, (0, 170, 228), slider_rect, 0, 10)

	slider_x=slider_rect.left+slider_rect.width*slider_percent
	pygame.draw.rect(screen, "grey", (slider_x, slider_rect.top, SCREEN_WIDTH-slider_x-10, slider_rect.height), 0, 10)
	pygame.draw.circle(screen, "white", (slider_x, slider_rect.centery), 10,0)
	pygame.draw.circle(screen, "black", (slider_x, slider_rect.centery), 10,1)
	
	slider2_y=slider2_rect.top+slider2_rect.height*steepness_percent
	pygame.draw.rect(screen, (0, 170, 228), slider2_rect, 0, 10)
	pygame.draw.rect(screen, "grey", (slider2_rect.left, slider2_y, 10, SCREEN_HEIGHT-slider2_y-20), 0, 10)
	pygame.draw.circle(screen, "white", (slider2_rect.centerx, slider2_y), 10,0)
	pygame.draw.circle(screen, "black", (slider2_rect.centerx, slider2_y), 10,1)

	pygame.display.flip()
