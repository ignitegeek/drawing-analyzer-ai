import cv2
import os

def analyze_drawing(image_path, output_folder):
    img = cv2.imread(image_path)
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)

    height, width = img.shape[:2]
    report = f"Detected {len(contours)} outer contours.\n"
    report += f"Drawing Size: {width} x {height} px\n"

    if len(contours) > 10:
        report += "\n⚠️ Drawing has complex geometry. Consider simplifying features."

    result_name = os.path.basename(image_path).replace("drawing_", "annotated_")
    result_path = os.path.join(output_folder, result_name)
    cv2.imwrite(result_path, output)
    return result_path, report
