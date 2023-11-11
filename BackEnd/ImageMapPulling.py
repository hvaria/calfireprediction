import os
import requests
from flask import Flask, request, Response


# Define the maximum allowable differences in latitude and longitude
# These are assumed values and might need adjustment based on actual API constraints
MAX_DIFF_LAT = 2.0  
MAX_DIFF_LONG = 2.0

def adjust_coordinates(cord):
    """
    Adjusts the given coordinates to ensure they fit within the 
    maximum allowable differences in latitude and longitude.
    
    Args:
    - cord (str): Comma-separated string of coordinates in the format 'lat1,long1,lat2,long2'
    
    Returns:
    - str: Adjusted coordinates in the same format
    """
    
    # Split the input coordinates and convert them to floats
    lat1, long1, lat2, long2 = map(float, cord.split(','))
    
    # Calculate the difference in latitudes and longitudes
    lat_diff = abs(lat2 - lat1)
    long_diff = abs(long2 - long1)

    # Adjust the latitudes if the difference exceeds the maximum allowable difference
    if lat_diff > MAX_DIFF_LAT:
        mid_lat = (lat1 + lat2) / 2
        lat1 = mid_lat - MAX_DIFF_LAT / 2
        lat2 = mid_lat + MAX_DIFF_LAT / 2

    # Adjust the longitudes if the difference exceeds the maximum allowable difference
    if long_diff > MAX_DIFF_LONG:
        mid_long = (long1 + long2) / 2
        long1 = mid_long - MAX_DIFF_LONG / 2
        long2 = mid_long + MAX_DIFF_LONG / 2

    # Return the adjusted coordinates as a comma-separated string
    return "{},{},{},{}".format(lat1, long1, lat2, long2)

def get_image(date, cord):
    adjusted_cord = adjust_coordinates(cord)
    url = 'https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&&CRS=EPSG:4326&WRAP=DAY&LAYERS=MODIS_Terra_CorrectedReflectance_Bands721&FORMAT=image/jpeg&HEIGHT=800&WIDTH=800&BBOX=' + adjusted_cord + '&TIME=' + date
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            # Define the folder path and image file name
            main_folder = 'data'
            sub_folder_path = os.path.join(main_folder, adjusted_cord.replace(',', '_'))
            image_name = 'Input_map_{}_{}.jpg'.format(date, adjusted_cord.replace(',', '_'))
            full_path = os.path.join(sub_folder_path, image_name)


            if not os.path.exists(sub_folder_path):
                os.makedirs(sub_folder_path)

            with open(full_path, 'wb') as f:
                f.write(response.content)
            return response.content




        # if response.status_code == 200:
        #     f_ext = 'Input_map_{}_{}.jpg'.format(date, adjusted_cord.replace(',', '_'))
            
        #     # Check and create directory if it doesn't exist
        #     directory = os.path.dirname(f_ext)
        #     if directory and not os.path.exists(directory):
        #         os.makedirs(directory)
            
        #     with open(f_ext, 'wb') as f:
        #         f.write(response.content)
        #     return response.content
        else:
            print("Error:", response.status_code)
            return None
            
    except requests.RequestException as e:
        print("Request error:", e)
        return 0
    
# def get_image(date, cord):
#     adjusted_cord = adjust_coordinates(cord)
#     # adjusted_cord = cord
#     url = 'https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&&CRS=EPSG:4326&WRAP=DAY&LAYERS=MODIS_Terra_CorrectedReflectance_Bands721&FORMAT=image/jpeg&HEIGHT=800&WIDTH=800&BBOX=' + adjusted_cord + '&TIME=' + date
    
#     response = requests.get(url, timeout=10)
#     if response.status_code == 200:
#         return response.content
#     else:
#         return None
    

def get_image_stream(date, cord):
    adjusted_cord = adjust_coordinates(cord)
    url = 'https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&&CRS=EPSG:4326&WRAP=DAY&LAYERS=MODIS_Terra_CorrectedReflectance_Bands721&FORMAT=image/jpeg&HEIGHT=800&WIDTH=800&BBOX=' + adjusted_cord + '&TIME=' + date
    
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        f_ext = 'Input_map_{}_{}.jpg'.format(date, adjusted_cord.replace(',', '_'))
        response_headers = {
            'Content-Type': 'image/jpeg',
            'Content-Disposition': 'inline; filename=image.jpg'
        }

        # Stream the image content as the response
        return Response(response.iter_content(chunk_size=1024), headers=response_headers)
    else:
        return "Failed to fetch the image from NASA Worldview API", 500


if __name__ == "__main__":
    image = get_image()
    process_image(image)

# def getImage(date, cord):
#     url = 'https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&&CRS=EPSG:4326&WRAP=DAY&LAYERS=MODIS_Terra_CorrectedReflectance_Bands721&FORMAT=image/jpeg&HEIGHT=800&WIDTH=800&BBOX='+ cord + '&TIME=' + date
#     print(url)
#     page = requests.get(url)
#     f_ext = 'Input_map.jpg'
#     with open(f_ext, 'wb') as f:
#         f.write(page.content)
        
#     return 1  