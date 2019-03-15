from PIL import Image, ImageDraw
import face_recognition
import base64
import io
import numpy as np
import json
def compute(image):
	# Load the jpg file into a numpy array
	# image = face_recognition.load_image_file(img)

	# Find all facial features in all the faces in the image
	face_landmarks_list = face_recognition.face_landmarks(image)

	print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

	# Create a PIL imagedraw object so we can draw on the picture
	pil_image = Image.fromarray(image)
	d = ImageDraw.Draw(pil_image)

	for face_landmarks in face_landmarks_list:

	    # Print the location of each facial feature in this image
	    for facial_feature in face_landmarks.keys():
	        print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))
	    wanted_features = ['chin',"left_eyebrow",'right_eyebrow']
	    # Let's trace out each facial feature in the image with a line!
	    for facial_feature in face_landmarks.keys():
	    	if facial_feature in wanted_features:
	        	d.line(face_landmarks[facial_feature], width=5)
	return pil_image

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/parse', methods=['GET', 'POST'])
def parse_request():
	print('chaS')
	if request.method == 'POST':
		image = base64.decodebytes(bytes(request.get_json(force=True)['Image'], 'utf-8'))
		img = Image.open(io.BytesIO(image))
		img = img.convert("RGB")
		image = compute(np.array(img))
		image.save("11.jpg")
		return json.dumps({'Image': im_2_b64(image)})
def im_2_b64(image):
    buff = io.BytesIO()
    image.save(buff, format="JPEG")

    img_str = base64.b64encode(buff.getvalue())
    new_str = img_str.decode('utf-8')
    return new_str
if __name__ == '__main__':
	app.run(host = '0.0.0.0')