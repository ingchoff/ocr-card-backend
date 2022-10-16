import cv2
import imutils
import numpy as np
from google.cloud import vision

def align_images(image, template):
  # convert both the input image and template to grayscale
  imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
  
  # use ORB to detect keypoints and extract (binary) local
  # invariant features
  sift = cv2.SIFT_create()
  keypoints1, descriptors1 = sift.detectAndCompute(imageGray, None)
  keypoints2, descriptors2 = sift.detectAndCompute(templateGray, None)
  
  # match the features
  bf = cv2.BFMatcher()
  matches = bf.knnMatch(descriptors1, descriptors2, k=2)
  
  # sort the matches by their distance (the smaller the distance,
  # the "more similar" the features are)
  good_matches = []
  for m, n in matches:
    if m.distance < 0.7 * n.distance:
      good_matches.append([m])
  # check to see if we should visualize the matched keypoints
  matchedVis = cv2.drawMatchesKnn(image, keypoints1,template, keypoints2, good_matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
  matchedVis = imutils.resize(matchedVis, width=1000)
  # cv2.imshow("Matched Keypoints", matchedVis)
  points1 = np.float32([keypoints1[m[0].queryIdx].pt for m in good_matches])
  points2 = np.float32([keypoints2[m[0].trainIdx].pt for m in good_matches])

  (h, mask) = cv2.findHomography(points1, points2, method=cv2.RANSAC)
  height, width, channels = template.shape
  aligned = cv2.warpPerspective(image, h, (width, height))
  return aligned

def ocr(card_image):
  client = vision.ImageAnnotatorClient()
  image = vision.Image(content=card_image)
  response = client.text_detection(image=image)
  texts = response.text_annotations
  return texts
