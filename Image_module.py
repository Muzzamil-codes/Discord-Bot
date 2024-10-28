from PIL import Image, ImageDraw, ImageFont

def create_text_image(text, output_path="text_image.png"):
    target_width, target_height = 358, 100
    font_path = "arial.ttf"
    font_size = 100
    font = ImageFont.truetype(font_path, font_size)
    bouding_box = font.getbbox(text)
    text_width = bouding_box[2] - bouding_box[0]
    text_height = bouding_box[3] - bouding_box[1]
    
    while text_width > target_width or text_height > target_height:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        bouding_box = font.getbbox(text)
        text_width = bouding_box[2] - bouding_box[0]
        text_height = bouding_box[3] - bouding_box[1]

    text_image = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)
    text_x = (target_width - text_width) // 2
    text_y = (target_height - text_height) // 2
    draw.text((text_x, text_y), text, font=font, fill="black")
    text_image.save(output_path)
    return output_path

def Image_maker(text, base_image_path="s_image.png", output_path="created_image.png"):
    text_image_path = create_text_image(text)
    base_image = Image.open(base_image_path).convert("RGBA")
    text_image = Image.open(text_image_path).convert("RGBA")
    rotated_text = text_image.rotate(47, resample=Image.BICUBIC, expand=True)
    base_image.paste(rotated_text, (165, 740), rotated_text)
    base_image.save(output_path)
    return output_path

