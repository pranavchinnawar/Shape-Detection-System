import cv2

# Read Image
img = cv2.imread("Projects/Shape-Detection-System/images/shapes.png")

if img is None:
  print("Error: Image not found!")
  exit()


# Copy image for drawing
output = img.copy()


# Convert to Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Apply Gaussian Blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)


# Apply Threshold
_, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)


# Find Contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
shape_count = 0


# Process Every Contour
for contour in contours:
  
    #Ignore tine noise
    area = cv2.contourArea(contour)

    if area < 500:
       continue

    shape_count += 1

    perimeter = cv2.arcLength(contour, True)

    # Approximate contour
    epsilon = 0.02 * perimeter

    approx = cv2.approxPolyDP(contour, epsilon, True)
    corners = len(approx)

    # Bounding Rectangle
    x, y, w, h = cv2.boundingRect(approx)

    # Detect Shape
    if corners == 3:
       shape = "Triangle"
    elif corners == 4:
        aspect_ratio = w / float(h)
        if 0.95 <= aspect_ratio <= 1.05:
            shape = "Square"
        else:
           shape = "Rectangle"
    elif corners == 5:
        shape = "Pentagon"
    elif corners == 6:
        shape = "Hexagon"
    else:
       shape = "Circle"


    #Draw Contour
    cv2.drawContours(output, [approx], -1, (255, 0, 0), 3)

    # Draw Bounding Rectangle
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display Shape Name
    cv2.putText(output, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display Number of Corners
    cv2.putText( output, f"Corners: {corners}", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)


    # Print Information
    print("=" * 40)
    print(f"Shape {shape_count}")
    print(f"Detected Shape : {shape}")
    print(f"Corners        : {corners}")
    print(f"Area           : {area:.2f}")
    print(f"Perimeter      : {perimeter:.2f}")
    
print("=" * 40)
print(f"Total Shapes Detected : {shape_count}")


# Save Output
cv2.imwrite("Projects/Shape-Detection-System/output/result.png", output)

# Show Images
size = (600, 400)

cv2.imshow("Original", cv2.resize(img, size))
cv2.imshow("Gray", cv2.resize(gray, size))
cv2.imshow("Blur", cv2.resize(blur, size))
cv2.imshow("Threshold", cv2.resize(thresh, size))
cv2.imshow("Shape Detection", cv2.resize(output, size))

cv2.waitKey(0)
cv2.destroyAllWindows()