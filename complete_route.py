# Go in a north,south,east,west sequence and always and return to origin point
import random


class CompleteRoute:
    def __init__(self, desired_distance) -> None:
        self.desired_distance = desired_distance
        self.traveled_distance = 0
        self.direction_sequence = []
        self.base_directions = ["north", "south", "east", "west"]
        self.n_s = ["north", "south"]
        self.e_w = ["east", "west"]

    def move_sequence(self):

        """Create sequence of alternating north/east/south/west configurations so that the the sequence always points back to the origin"""

        for _ in range(len(self.base_directions)):

            if self.direction_sequence == []:

                moving_direction = random.choice(
                    [direction for direction in self.base_directions]
                )

            elif self.direction_sequence[-1] in self.n_s:
                moving_direction = random.choice(
                    [
                        direction
                        for direction in self.e_w
                        if direction not in self.direction_sequence
                    ]
                )

            else:
                moving_direction = random.choice(
                    [
                        direction
                        for direction in self.n_s
                        if direction not in self.direction_sequence
                    ]
                )

            self.direction_sequence.append(moving_direction)

    def move_distance(self):

        """Assign a random choice between 0.25 (abstractly, miles) to a maximum of 40% self.distance. This will represent the 'out and back' for one direction pair. Then, subtract double that number (self.traveled distance) over the remainder of (self.desired_distance - self.traveled_distance)."""

        move_1 = round(random.uniform(0.25, (self.desired_distance * 0.40)), 2)
        self.traveled_distance += move_1 * 2

        move_2 = round((self.desired_distance - (move_1 * 2)) / 2, 2)
        self.traveled_distance += move_2 * 2

        return move_1, move_2

    def move_assignment(self, move_1, move_2):

        """Assign move_1, move_2 to the distance pairs as a random choice. Save in a dictionary"""

        dist_dict = {}

        distance_pair1 = self.direction_sequence[0::2]
        distance_pair2 = self.direction_sequence[1::2]

        for i in range(0, len(self.direction_sequence) // 2):
            dist_dict[distance_pair1[i]] = move_1
            dist_dict[distance_pair2[i]] = move_2

        return dist_dict

    def print_route(self, dist_dict):

        """Simply print the direction and, distance (miles) traveled in order"""
        print(f"This route will start out going {self.direction_sequence[0]} \n")

        for key, value in dist_dict.items():
            print(f"Traveling {key} for {value} miles...")

        print(f"\nCongratulations! We made it back to where we started!")
        print(
            f"You requested to travel {self.desired_distance} miles and the route took you {self.traveled_distance} miles."
        )  # for future integration into openmaps API


my_route = CompleteRoute(3)

my_route.move_sequence()
move_1, move_2 = my_route.move_distance()
dist_dict = my_route.move_assignment(move_1, move_2)
my_route.print_route(dist_dict)
