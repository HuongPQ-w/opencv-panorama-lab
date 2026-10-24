import cv2
import os
import re

# Image folder
image_folder = "image"
image_extensions = ('.jpg', '.jpeg', '.png')

# Get image files and sort by number in filename
image_files = sorted(
    [
        f for f in os.listdir(image_folder)
        if f.lower().endswith(image_extensions)
    ],
    key=lambda x: int(re.search(r'\d+', x).group())
)

# Load images
images = []
for file_name in image_files:
    full_path = os.path.join(image_folder, file_name)
    img = cv2.imread(full_path)
    if img is not None:
        images.append(img)
    else:
        print(f"Cannot read image: {full_path}")

# Check number of images
if len(images) < 2:
    print("At least 2 images are required for panorama stitching.")
    exit()

print("Processing panorama...")

# Create stitcher
stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)

# Stitch images
status, panorama = stitcher.stitch(images)

# Check result
if status == cv2.Stitcher_OK:

    cv2.imwrite("panorama_result.jpg", panorama)

    print("Panorama stitching completed successfully.")
    print("Output saved as: panorama_result.jpg")

    # Resize for display
    max_width = 1200
    h, w = panorama.shape[:2]
    scale = max_width / w
    resized = cv2.resize(
        panorama,
        (int(w * scale), int(h * scale))
    )
    cv2.imshow("Panorama Result", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(f"Stitching failed (Error Code: {status})")
    if status == 1:
        print("ERR_NEED_MORE_IMGS")
        print("- Not enough overlap between images")
        print("- Incorrect image order")
    elif status == 2:
        print("ERR_HOMOGRAPHY_EST_FAIL")
        print("- Failed to estimate homography")
        print("- Images may be too different")
    elif status == 3:
        print("ERR_CAMERA_PARAMS_ADJUST_FAIL")
        print("- Failed to adjust camera parameters")