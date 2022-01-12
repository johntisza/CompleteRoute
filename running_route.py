import random
import os
import requests
import openrouteservice as ors
from openrouteservice import convert
from time import sleep

from browser_route import Browser


ors_key = os.environ["ORS_KEY"]
# must request key from OpenRouteService, then put in your operating system environment variables. !!!DO THIS FIRST!!!

client = ors.Client(key=ors_key)


class RunningRoute:
    def __init__(self) -> None:
        self.lon = -87.678022  # use your latitude
        self.lat = 41.953227  # use your longitude
        self.distance = 0
        self.random_seed = 0

    def ask_distance(self):

        """Request distance in miles via terminal input"""

        miles = int(input("How many miles would you like to run today? "))
        self.distance = miles * 1609.34  # convert to meters

    def pick_random_seed(self):

        """Selects seed to initialize random route"""

        self.random_seed = random.randint(0, 200)  # same as website

        return self.random_seed

    def create_credentials(self):

        """Credentials to query the OpenRouteService API"""

        self.body = {
            "coordinates": [[self.lon, self.lat]],
            "instructions": "True",
            "units": "mi",
            "options": {
                "round_trip": {
                    "length": self.distance,
                    "points": 4,
                    "seed": self.random_seed,
                }
            },
        }

        self.headers = {
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            "Authorization": ors_key,
            "Content-Type": "application/json; charset = utf-8",
        }

        return self.body, self.headers

    def post_request(self):

        """Posts requests to OpenRouteService API"""

        call = requests.post(
            f"https://api.openrouteservice.org/v2/directions/foot-walking",
            json=self.body,
            headers=self.headers,
        )

        this_route = call.json()["routes"][0]

        try:
            if (
                len(this_route["segments"][0]["steps"]) >= 20
                or len(this_route["segments"][0]["steps"]) == 0
            ):
                self.pick_random_seed()
                self.create_credentials()
                self.post_request()

            elif (
                len(this_route["segments"][0]["steps"]) < 20
            ):  # google maps maximum waypoints
                step_info = this_route["segments"][0]["steps"]

                total_distance = this_route["segments"][0]["distance"]
                geometry = this_route["geometry"]

                print(
                    f"Sucessful route found! It only took {len(step_info)} steps and a total distance of {total_distance} miles!"
                )

                self.geometry = geometry
                self.step_info = step_info

        except (KeyError, AttributeError) as e:
            pass

    def get_step_set(self):

        """Creates points only at turns in route"""

        step_set = set()

        for i in range(0, len(self.step_info)):

            waypoints = self.step_info[i]["way_points"][-1]

            step_set.add(waypoints)

        step_set = sorted(step_set)

        return step_set

    def decode_geometry(self):

        """Decodes polyline hash(?) into coordinate list"""

        decoded_coords = convert.decode_polyline(self.geometry)

        return decoded_coords["coordinates"]

    def select_coords(self, step_set: set, coords: list):

        """Ensures that start/stop coordinates are the same, then appends all steps in between"""

        optimized_list = []
        optimized_list.append(coords[0])  # starting coords

        for step in step_set:
            optimized_list.append(coords[step])  # other steps

        return optimized_list

    def reverse_lat_lon(self, coords):

        """Reverses lat/long to be in line with Google Maps system"""

        lat = [coordinate_pair[1] for coordinate_pair in coords]
        lon = [coordinate_pair[0] for coordinate_pair in coords]
        new_coords = list(zip(lat, lon))

        final_coords = "/".join(map(lambda x: str(x[0]) + "," + str(x[1]), new_coords))

        print(f"www.google.com/maps/dir/{final_coords}")

        return final_coords

    def main(self):

        self.ask_distance()
        self.pick_random_seed()
        self.create_credentials()
        self.post_request()
        step_set = self.get_step_set()
        coords = self.decode_geometry()
        optimized_coords = self.select_coords(step_set, coords)

        final_coords = self.reverse_lat_lon(optimized_coords)

        return final_coords


if __name__ == "__main__":

    rr = RunningRoute()
    final_coords = rr.main()
    sleep(2)
    chrome_browser = Browser(final_coords)
    chrome_browser.main()
