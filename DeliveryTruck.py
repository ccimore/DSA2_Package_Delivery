import datetime


# Blueprint for truck objects
# O(N)time --- O(N)space
class DeliveryTruck:
    def __init__(self, initial_clock):
        self.package_load = []
        self.address = "4001 South 700 East"
        self.initial_clock = initial_clock
        self.home = "4001 South 700 East"
        self.clock = initial_clock
        self.destinations_visited = 0
        self.package_max = 16
        self.velocity = 18
        self.miles = 0.0

    # returns time it takes to drive distance
    # O(1)time --- O(1)space
    def drive_time(self, distance):
        time = datetime.timedelta(hours=distance / self.velocity)
        return time

    # Updates truck instance fields
    # O(1)time --- O(1)space
    def update_truck(self, address, distance):
        self.miles += distance
        self.address = address
        self.clock += self.drive_time(distance)
        self.destinations_visited += 1

    # Retrieves earliest driver back to base for next truck
    # O(1)time --- O(1)space
    def truck_driver_ready(self, delivery_truck1, delivery_truck2):
        ready_time = min(delivery_truck1.clock, delivery_truck2.clock)
        self.initial_clock = ready_time
        self.clock = ready_time
