from PIL import Image
def generate_low_quality_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((800, 600))
    low_quality_image_path = image_path.replace('.jpg', '_low.jpg')
    image.save(low_quality_image_path, 'JPEG', quality=50)
    return low_quality_image_path