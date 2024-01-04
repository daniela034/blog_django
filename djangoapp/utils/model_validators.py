from django.core.exceptions import ValidationError

# validator para as imagens que queremos colocar no favicon
def validate_png(image):
    if not image.name.lower().endswith('.png'): 
        raise ValidationError('Image needs to be .png')
                