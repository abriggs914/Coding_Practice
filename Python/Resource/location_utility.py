import geocoder
import geopy
from geopy.geocoders import Nominatim
import asyncio
import winsdk.windows.devices.geolocation as wdg


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


VERSION = \
    """	
        General Utility functions for location.
        Version...........1.02
        Date........2023-02-15
        Author....Avery Briggs
    """


def VERSION_NUMBER():
    return float(VERSION.split("\n")[2].split(".")[-2] + "." + VERSION.split("\n")[2].split(".")[-1])


def VERSION_DATE():
    return VERSION.split("\n")[3].split(".")[-1]


def VERSION_AUTHOR():
    return VERSION.split("\n")[4].split(".")[-1]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def get_device_gps_coords():
    """Using windows SDK, retrieve device's GPS location."""

    async def async_device_gps():
        locator = wdg.Geolocator()
        pos = await locator.get_geoposition_async()
        return [pos.coordinate.latitude, pos.coordinate.longitude]

    try:
        return asyncio.run(async_device_gps())
    except PermissionError:
        msg = "ERROR: You need to allow applications to access you location in Windows settings"
        print(msg)
        return msg, ""



def get_ip_coords():
    """Using GeoCoder, retrieve device's IP Latitude and Longitude."""
    return geocoder.ip('me').latlng


def coords_to_location(lat, lng):
    """Using GeoPy, reverse look-up a Latitude and Longitude, returning a Location object.

    # attributes: 'address', 'latitude', 'longitude', 'altitude', 'point', 'raw'
    # use raw["address"] for a dict of keys ['road', 'county', 'state', 'ISO3166-2-lvl4', 'country', 'country_code']
    """
    return Nominatim(user_agent="GetLoc").reverse(f"{lat}, {lng}")


def coords_to_address(lat, lng):
    """Using GeoPy, reverse look-up a Latitude and Longitude, returning a string representation of the address."""
    return Nominatim(user_agent="GetLoc").reverse(f"{lat}, {lng}").address


def company_from_location(location_in=None):
    """Based on device's GPS location, return the company for that province.
    Pass a geoPy.Location object to bypass async call."""
    if location_in is None:
        location = coords_to_location(*get_device_gps_coords())
        province = location.raw["address"]["state"]
    else:
        assert isinstance(location_in, geopy.Location), f"Error, param 'location_in' must be a geoPy.Location object. Got '{location_in}', {type(location_in)=}"
        province = location_in.raw["address"]["state"]
    match province:
        case 'New Brunswick / Nouveau-Brunswick':
            return "BWS"
        case 'Ontario':
            return "Stargate"
        case 'Quebec':
            return "Lewis"
    # print(f"{province=}, {location=}, {type(location)=}")
    return "UNKNOWN"


if __name__ == '__main__':

    # print(f"{get_ip_coords()=}")
    # print(f"{get_device_gps_coords()=}")
    # print(f"{coords_to_location(*get_ip_coords())=}")
    # print(f"{coords_to_location(*get_device_gps_coords())=}")
    # print(f"{coords_to_location(*get_device_gps_coords()).raw['address']=}")
    # print(f"{list(coords_to_location(*get_device_gps_coords()).raw['address'].keys())=}")
    # print(f"{coords_to_address(*get_ip_coords())=}")
    # print(f"{coords_to_address(*get_device_gps_coords())=}")
    print(f"{company_from_location()=}")

