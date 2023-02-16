from location_utility import *
import datetime
import time


# if __name__ == "__main__":
	
out_file = "C:\Access\output_location.txt"
with open(out_file, "w") as f:
	location = coords_to_location(*get_device_gps_coords())
	f.write(f"DateCreated={datetime.datetime.now():%Y-%m-%d %H:%M}\n")
	f.write(f"{location=}\n")
	f.write(f"{company_from_location(location)=}\n")

print(f"file '{out_file}' created successfully.")