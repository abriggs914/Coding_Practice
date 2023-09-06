import geocoder
from geopy.geocoders import Nominatim
import asyncio
import winsdk.windows.devices.geolocation as wdg
from gps import gps, WATCH_ENABLE
import time
import win32api


if __name__ == '__main__':

    #  IP address location

    g = geocoder.ip('me')
    latlng = g.latlng
    print(latlng)

    # calling the nominatim tool
    geoLoc = Nominatim(user_agent="GetLoc")

    # passing the coordinates
    # locname = geoLoc.reverse("26.7674446, 81.109758")


    async def getCoords():
        locator = wdg.Geolocator()
        pos = await locator.get_geoposition_async()
        return [pos.coordinate.latitude, pos.coordinate.longitude]


    def getLoc():
        try:
            return asyncio.run(getCoords())
        except PermissionError:
            print("ERROR: You need to allow applications to access you location in Windows settings")


    # print(f"{get_device_gps_coords()=}")
    latlng = getLoc()
    locname = geoLoc.reverse(f"{latlng[0]}, {latlng[1]}")

    # printing the address/location name
    print(f"{locname.address=}")

    #
    #
    # gps = gps(game_mode=WATCH_ENABLE)
    # lock = False
    # while not lock:
    #     report = gps.next()
    #     # 3D Fix
    #     if report['class'] == 'TPV' and report['game_mode'] == 3:
    #         print(report.lon)
    #         print(report.lat)
    #         print(report.alt)
    #         print(report.speed)
    #         print(report.track)
    #         print(report.climb)
    #     else:
    #         time.sleep(5)
