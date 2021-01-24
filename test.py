from PIL import Image, ImageDraw, ImageFont
import textwrap




image=Image.open("utils/Images/star-wars-background.jpg") 
image_size=(-1, -1), 
font_path='utils/Custom_Fonts/star-jedi-font/StarJedi.ttf'
font_size=30
text_color=(255, 232, 31) # star wars yellow
bg_color=(0, 0, 0)
text='''shopshop shop shopshopshopshops
hopshopshopshopshop shopshopshopshopshopsh
opshopshopsh'''
image_width, image_height = image.size
break_point = 75/100 * image_width




jumpsize = 60
#font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)
font = ImageFont.truetype(font=font_path, size=font_size)

# text wrapping
char_width, char_height = font.getsize('A')
chars_per_line = image_width // char_width
text = textwrap.wrap(text, width=chars_per_line)[0]

# while True:
#     if font.getsize(text)[0] < break_point:
#         font_size += jumpsize
#     else:
#         jumpsize = jumpsize // 2
#         font_size -= jumpsize
#     font = ImageFont.truetype(font=font_path, size=font_size)
#     if jumpsize <= 1:
#         break

draw=ImageDraw.Draw(image)
w, h = draw.textsize(text, font)
#if '\n' in text:
draw.multiline_text(((image_width - w) / 2, (image_height - h) / 2 ), text,fill= text_color, font=font, stroke_width=3, stroke_fill='black', align="center")
#draw.text(((image_width - w) / 2, (image_height - h) / 2 ), text,fill= text_color, font=font, stroke_width=3, stroke_fill='black', align="center")
# else:
#     draw.text(((image_size[0] - w) / 2, (image_size[1] - h) / 2), text, text_color, font)

#return image
image.show()

#centered_text = TextOnCenter(image=myimg, font_size=80, text="2")
#centered_text.draw_text()
#centered_text.show()
#centered_text.get_image().save("with_text.jpg")

