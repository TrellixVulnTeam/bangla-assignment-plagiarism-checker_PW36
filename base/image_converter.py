
import pytesseract
from PIL import Image
class ImageConverter:

    def convert(self, images): 
        full_text = ''
        for image in images:
            text = pytesseract.image_to_string(Image.open(image), lang="ben")
            full_text += text.replace('\n', ' ')
        return full_text