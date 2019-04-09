from PIL import Image
from skimage import io
from skimage.measure import compare_ssim as ssim


def get_ssim(file1, file2):
    image1 = io.imread(file1)
    image2 = io.imread(file2)
    similarity = ssim(image1, image2, multichannel = True)

    return similarity


def is_white(file_path):
    image = Image.open(file_path)
    image = image.convert('L')
    histogram = image.histogram()
    bw_rate = sum(histogram[0:20]+histogram[-20:]) / sum(histogram)
    if bw_rate >= 0.9:
        return True
    return False