import ImageMapPulling
import svm_test  # Assuming this is a module you have imported
# import YoloDetection  # Assuming this is a module you have imported
import sys

def main():
    # Check if sufficient command-line arguments are provided
    if len(sys.argv) < 6:
        print("Usage: python script.py latitude1 longitude1 latitude2 longitude2 date")
        sys.exit(1)

    latitude1 = sys.argv[1]
    longitude1 = sys.argv[2]
    latitude2 = sys.argv[3]
    longitude2 = sys.argv[4]
    date = sys.argv[5]

    co_ordinates = latitude1 + ',' + longitude1 + ',' + latitude2 + ',' + longitude2

    image = ImageMapPulling.get_image(date, co_ordinates)
    if image:
        # image_path = "Input_map.jpg"
        print("Image is Pulled")

# need to change this resultstr to a response json containing "fire detected" value and image as bytes

        resultstr = svm_test.isFireDetected(image)
        print("SVM output is: ", resultstr)
        if resultstr == "Fire Detected":
            print("FIRE IS DETETED FOR THE GIVEN CO-ORDINATES and GIVEN DATES")
            # YoloDetection.startYolo(image_path)
        else:
            print("FIRE IS NOT-DETETED FOR THE GIVEN CO-ORDINATES and GIVEN DATES")

if __name__ == "__main__":
    main()