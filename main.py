import cv2
import numpy as np

image = cv2.imread('fin.webp')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)

edges = cv2.Canny(blurred, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

seat_count = 0

for contour in contours:
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) == 4:
        seat_count += 1
        cv2.drawContours(image, [approx], 0, (0, 255, 0), 3)

print(f"Number of seats detected: {seat_count}")

cv2.imshow('Detected Seats', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
