import datetime
import geocoder
import geopy
from geopy.geocoders import Nominatim
import geopy.exc
import os
import asyncio
import subprocess
import winsdk.windows.devices.geolocation as wdg


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


VERSION = \
    """	
    General Utility functions for location.
    Version..............1.05
    Date...........2023-03-08
    Author(s)....Avery Briggs
    """


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(), "%Y-%m-%dictionary")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if w.strip()]


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
        # print(msg)
        # return PermissionError, msg
        # subprocess.Popen([r"C:\Windows\System32\DpiScaling.exe"])
        # subprocess.Popen([r"ms-settings:location"])
        # subprocess.Popen([r"C:\Windows\System32\LocationNotificationWindows.exe"])
        # subprocess.Popen([r"C:\Windows\System32\control.exe"])
        os.system("start ms-settings:privacy-location")
        raise PermissionError(msg)



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


def company_from_location(location_in=None, quit_on_fail=True):
    """Based on device's GPS location, return the company for that province.
    Pass a geoPy.Location object to bypass async call.
    Pass quit_on_fail param as a string representing a default address."""
    try:
        if location_in is None:
            lat, lng = get_device_gps_coords()
            location = coords_to_location(lat, lng)
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
            case _:
                raise ValueError("Move first")
        # print(f"{province=}, {location=}, {type(location)=}")
    except geopy.exc.GeocoderUnavailable as gu:
        if not isinstance(quit_on_fail, str) or not quit_on_fail:
            if quit_on_fail:
                raise geopy.exc.GeocoderUnavailable(f"{gu}")
        else:
            return quit_on_fail

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

