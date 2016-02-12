import cv2

def read_image_white_text(file_path):
	
	image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
	th , dst = cv2.threshold(image , 130 , 255 ,cv2.THRESH_BINARY_INV)
	file_path  = 'white_text.jpg'
	cv2.imwrite(file_path , dst)
	return file_path

