from location_utiility import *


if __name__ == "__main__":
	
	with open("output_loaction.txt", "w") as f:
		location = coords_to_location(*get_device_gps_coords())
		f.write(f"{location=}")
		f.write(f"{company_from_location(location)=}")