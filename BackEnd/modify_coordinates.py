import geopy
from geopy import distance


# expands a single coordinate input to a bottom left coord and top right coord
def expand_single_coord(original_lat, original_lon):

    # geopy 'destination' function documentation here: https://geopy.readthedocs.io/en/stable/#:~:text=calculate%20destination%20point%20using%20a%20starting%20point%2C%20bearing%20and%20a%20distance.%20this%20method%20works%20for%20non-abstract%20distances%20only.

    bottom_left = geopy.distance.distance(kilometers=70).destination((original_lat, original_lon), 225)
    top_right = geopy.distance.distance(kilometers=70).destination((original_lat, original_lon), 45)

    return(bottom_left.latitude, bottom_left.longitude, top_right.latitude, top_right.longitude)



def test_expand_single_coord():
    test_lat = 40.447368
    test_lon = -120.676757
    
    bl_lat, bl_lon, tr_lat, tr_lon = expand_single_coord(test_lat, test_lon)
    output = f'{bl_lat} {bl_lon} {tr_lat} {tr_lon}'
    if (output == '40.00014281254964 -121.25639388506238 40.89161369210514 -120.08941073614328'):
        print('test_expand_single_coord PASSED')
    else:
        print('test_expand_single_coord FAILED')
    # url = f'https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&&CRS=EPSG:4326&WRAP=DAY&LAYERS=MODIS_Terra_CorrectedReflectance_Bands721&FORMAT=image/jpeg&HEIGHT=600&WIDTH=600&BBOX={bl_lat},{bl_lon},{tr_lat},{tr_lon}&TIME=2020-08-26'
    # print(f'{bl_lat} {bl_lon} {tr_lat} {tr_lon}')
    # print(url)
