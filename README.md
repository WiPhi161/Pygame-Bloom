# Pygame-Bloom
A really simple implementation of the bloom effect in python

![example screenshot](https://user-images.githubusercontent.com/100654058/215316974-c96fdf09-01a7-4355-910f-53913a000d53.png)

Inspired by this youtube video by SimonDev: https://www.youtube.com/watch?v=ml-5OGZC7vE&t=565s

The most basic example of the bloom effect consists of 3 main steps:
1. Binary Threshold/Grayscaling the Image
2. Applying a Box Blur to the result of binary threshold. This should result in a blurry black and white image highlight the bright spots of the image
3. Adding the bloom mask to the original image

## Binary Threshold/Grayscaling the Image
Initially I used the simple method of averaging the RGB values of each pixel to procude a grayscale image, however this resulted in a burntout bloom effect where areas of the image where unnecessarily bright.

![global bloom](https://user-images.githubusercontent.com/100654058/215317348-c3835436-5420-401b-bea8-f58acaa0afc9.png)

*Global bloom from grayscaling*

Next I tried simpily binary thresholding the pixel values. Any pixel with a grayscale value over 128 would be rounded to (255,255,255), pure white, and vice-versa, any value under 128 would be rounded to (0,0,0), pure balck. This worked well, however, the contrast between bloomed areas and un-bloomed areas was very obvious, there was no smooth transtion what-so-ever. 

![image](https://user-images.githubusercontent.com/100654058/215317873-ad1744db-da99-48c3-bdba-29c9a519d1e6.png)

*Binary Threshold bloom*

I decided I need more control over how the brightness the image was attenuated. To acheive this, i needed to use a sigmoid function. A sigmoid function is a function that can interpolate values from 0 to 1 smoothly. Additionally, a sigmoid function allows me to control the speed of the transitions, as well as the cut-off value.

![image](https://user-images.githubusercontent.com/100654058/215318005-53fd468a-be85-47dd-bb20-63d8e33f4a6a.png)

*A logistic sigmoid function*

##The Box Blur

Generally, the easiest way to blur an image is to apply a "rolling kernel" or box, that averages the pixel values of neighbouring pixel.

![image](https://user-images.githubusercontent.com/100654058/215318367-0c69b99b-c026-432d-b177-dfc38efc6d24.png)

*Box Blur Kernel - credit: https://youtu.be/ml-5OGZC7vE?t=186*

Suprisingly, applying the box blur on horizontally and vertically neighbouring pixels simulatneously, creates a box-like artifacts in the final image. So, to avoid this, the box blur is applied to horizontal neighbours seperately, then the same is done to the vertical neighbours. When the box blur is applied to an image multipe times, it makes the image more blurry, and the resulting bloom effect more noticely. I decided 5 iterations was enough, as perform the box blur on each individual pixel (especially in python), is an expensive operation.

## Applying the bloom effect to the final image

After all these effort, box blurring and binary thresholding shenanigans, this is what we get:

![image](https://user-images.githubusercontent.com/100654058/215318795-b823bbb6-8299-421f-8e3f-f4165f7da12c.png)

Anticlimatic, I know, but we're almost there. The final step is to add the original image with this "bloom mask" that we have. The areas that need to bloomed get brighter, and the darker areas are left untouched. Thankfully, pygame has a super helpful blitting function with special flags, one of them being BLEND_RBG_ADD, which does exactly as it says. Instead of covering one image with another, its blends the two images, which in this case is exactly what we want.
```python
res_image.blit(box_blur(binary_threshold(img)), (0,0), special_flags=pygame.BLEND_RGB_ADD)
```

##Finishing touches

To make the example more interactive, I added sliders that controll specifically however the bloom is applied. The bottom slider controls the brightness cutoff, to the far right it includes everything, flooding the image with bloom, but to the far left, its excludes everything, applying no bloom. The slider on the left controls the steepness or how smoothly bright areas are blended with dark areas. At the very top, all the bloom is blended smoothly, blooming everything. At the very bottom, only the bright patches are bloomed and everthing else it left untouched. If I were to give it name, I think the most accurate label would be 'Brightness Contrast'. 


Well those are more than enough words from me. Please feel free to try out and tinker with this project. Happy coding!

