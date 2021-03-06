import re

import cv2
from PIL import Image

import reading_white_text
import smooth_image
from menu_parser import pytesser

INVERT_COLOR_THRESHOLD = 128


def make_string_alphanmeric(lines):
    s = re.sub('[^0-9a-zA-Z\n]+', ' ', lines)
    return s


def greyscale_image_mean(file_name):
    size = 128, 128
    im = Image.open(file_name)
    im.thumbnail(size)
    im.save('thumbnail.jpg', "JPEG")
    img = cv2.imread('thumbnail.jpg', 0)
    avg = 0
    x, y = im.size
    for i in range(y):
        for j in range(x):
            avg += img[i][j]
    return float(avg * 1.0 / (128 * 128))


D = {}


def remove_too_many_small_words_dish(text):
    new_text = []
    for lines in text:
        word_count = 0.0
        small_word_count = 0.0
        line = lines.split(' ')
        for word in line:
            if len(word) <= 2:
                small_word_count += 1
            word_count += 1
        try:
            small_word_proportion = small_word_count / word_count

        except:
            small_word_proportion = 0.0
        # print 'small_word_proportion: ' , small_word_proportion
        if small_word_proportion <= 0.4:
            new_text.append(line)

    return new_text


def fact(l):
    if l >= 500:
        return 1
    else:
        f = 500.0 / l
        if int(f) <= 0:
            return 1
        return int(f)


def image_process_extract_string(s, mask, x, y, w, h):
    im = mask[y: y + h, x: x + w]
    cv2.imwrite(s, im)
    size = 2 * w, 2 * h
    im = Image.open(s)
    im_resized = im.resize(size, Image.ANTIALIAS)
    im_resized.save(s, dpi=(100, 100))
    return pytesser.image_to_string(s, 6)


def extract_image(file_name):
    img = cv2.imread(file_name)
    # img_final = cv2.imread(file_name)

    img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv_img = (255 - img2gray)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 2))

    dilated = cv2.dilate(inv_img, kernel, iterations=7)  # dilate
    type_image = dilated
    image, contours, hierarchy = cv2.findContours(type_image, cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_NONE)  # get contours
    _, contours, hierarchy = cv2.findContours(type_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

    ind = 0
    image_2_text = smooth_image.smooth2(file_name)
    print('----------')
    for contour in contours:
        print('----------')
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)
        # draw rectangle around contour on original image
        if w < 20 or h < 20:
            continue
        if w > 500 and h > 500:
            continue
        cv2.rectangle(img, (x, y), (x + w + 10, y + h + 10), (255, 0, 255), 2)
        s = '/tmp/' + str(ind) + '.tif'
        box_read = image_process_extract_string(s, image_2_text, x, y, w, h)
        D[(x, y)] = box_read
        ind += 1
    final_list2 = []
    for k, v in sorted(D.items()):
        list_new = str(v).split('\n')
        for l in list_new:
            final_list2.append(l)
    return final_list2


def pre_process_image(file_path):
    norm2dp_image_path = 'norm2dp.jpg'
    final_image_path = 'final_image_processed.jpg'
    im = Image.open(file_path)
    l, w = im.size
    factor = fact(l)
    size = int(factor * l), int(factor * w)
    im_resized = im.resize(size, Image.ANTIALIAS)
    im_resized.save(norm2dp_image_path, dpi=(200, 200))
    im_new = smooth_image.smooth2(norm2dp_image_path)
    cv2.imwrite(final_image_path, im_new)
    return final_image_path


def remove_numeric_part(s):
    return ''.join([token for token in s if not s.isdigit()])


def main(file_path):
    mean_grey_scale_value = greyscale_image_mean(file_path)
    if not mean_grey_scale_value > INVERT_COLOR_THRESHOLD:
        file_path = reading_white_text.read_image_white_text(file_path)
    file_path = pre_process_image(file_path)
    x = list(extract_image(file_path))
    x = remove_too_many_small_words_dish(x)
    for line in x:
        line = make_string_alphanmeric(str(line))
        line = remove_numeric_part(line)
        line = line.strip()
        if len(line) > 0:
            print (line)
main('test.jpg')
