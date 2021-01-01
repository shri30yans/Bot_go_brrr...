import textwrap

from PIL import Image, ImageDraw, ImageFont
#pylint: disable = all
# Ignoring all linter warnings in this program (unused variables). It is a linter warning.

def generate_meme(im,top_text,bottom_text='', font_path='/Custom_Fonts/impact1.ttf', font_size=8,stroke_width=5):
    # load image
    #im = image_path
    
    #im = add_margin(im, 200, 20, 20, 20,colour)
    
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size

    # load font
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)

    # convert text to uppercase
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # text wrapping
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # draw top lines
    y = 10
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
        y += line_height

    # draw bottom lines
    y = image_height - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
        y += line_height
    return im
    # save meme
    #im.save('meme-' + im.filename.split('/')[-1])

def add_text(im,top_text,bottom_text,x1,y1,x2,y2,font_path='/Custom_Fonts/impact1.ttf', font_size=8,stroke_width=5):
    # load image
    #im = image_path
    #im = add_margin(im, 200, 20, 20, 20,colour)
    
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size

    # load font
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)

    # convert text to uppercase
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # text wrapping
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # draw top lines
    #y = 10
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        #x = (image_width - line_width) / 2
        draw.text((x1, y1), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
        #y += line_height

    # draw bottom lines
    #y = image_height - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        #x = (image_width - line_width) / 2
        draw.text((x2, y2), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
        #y += line_height
    return im
    # save meme
    #im.save('meme-' + im.filename.split('/')[-1])
def add_text_height(im,top_text,bottom_text,y1,y2,font_path='Custom_Fonts/impact1.ttf', font_size=8,stroke_width=5):
    # load image
    #im = image_path
    
    #im = add_margin(im, 200, 20, 20, 20,colour)
    
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size

    # load font
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)

    # convert text to uppercase
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # text wrapping
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # draw top lines
    y = y1
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
        y += line_height

    # draw bottom lines
    y=y2
    #y = image_height - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
        y += line_height
    return im

def star_wars_font(text,font_path='/Custom_Fonts/StarJedi.ttf', font_size=8,stroke_width=5):
    # load image
    #im = image_path
    
    #im = add_margin(im, 200, 20, 20, 20,colour)
    im= Image.open("Utils/Images/star-wars-background.jpg")
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size

    # load font
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)

    # convert text to uppercase
    text = text.upper()

    # text wrapping
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(text, width=chars_per_line)

    # draw top lines
    y = 10
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
        y += line_height

    # draw bottom lines
    # y = image_height - char_height * len(bottom_lines) - 15
    # for line in bottom_lines:
    #     line_width, line_height = font.getsize(line)
    #     x = (image_width - line_width) / 2
    #     draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
    #     y += line_height
    #im.show()
    return im

def add_margin(pil_img, top, right, bottom, left,colour):
        width, height = pil_img.size
        new_width = width + right + left
        new_height = height + top + bottom
        result = Image.new(pil_img.mode, (new_width, new_height),colour)
        result.paste(pil_img, (left, top))
        
        return result