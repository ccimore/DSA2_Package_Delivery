# Press Shift+F10 to execute
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# C950 PA - A Delivery Routing Application

# Main class launches program

import DeliveryTruck
from CSVList import CSVList
from Graph import Graph
from Vertex import Vertex
from builtins import ValueError
import datetime
from Package import Package
from HashMap import HashMap

# list to track the total package deliveries
total_packages_list = []


# Source: WGU C950 - Webinar 3 - How to Dijkstra - Complete Python Code pdf
# https://srm--c.na127.visual.force.com/apex/coursearticle?Id=kA03x000000e1gECAQ
# Creates package objects from list, inserts them into HashMap, and appends them to total packages list
# O(N)time --- O(N)space
def load_package(package_list, package_hash):
    for p in package_list:
        id_ = int(p[0])
        address = p[1]
        city = p[2]
        state = p[3]
        zipcode = p[4]
        deadline_time = p[5]
        weight = p[6]
        note = p[7]
        package = Package(id_, address, city, state, zipcode, deadline_time, weight, note)
        total_packages_list.append(package)
        package_hash.insert(id_, package)


# Sorts packages and loads them onto trucks based on package deadline time and special instructions
# O(N^2)time --- O(N)space
def load_trucks(truck1_, truck2_, truck3_, package_list):
    # Create empty truck load lists and sort list
    truck1_load = []
    truck2_load = []
    truck3_load = []
    sort_list = []
    # Loop through package list and append to sort list
    for p in package_list:
        sort_list.append(p)
    # While sort list is not empty, sort packages to truck lists based on deadline time and special instructions
    while len(sort_list) > 0:
        for package_ in sort_list:
            # Check for "truck 2" in package note.  Add to truck 2 and remove from sort list.
            if "truck 2" in package_.note:
                truck2_load.append(package_.id_)
                sort_list.remove(package_)
            # Check for "Must be delivered" in package note. This indicates packages that must be delivered together.
            # Some of these are morning packages, so they go in truck 1.  Remove from sort list.
            elif "Must be delivered" in package_.note:
                truck1_load.append(package_.id_)
                sort_list.remove(package_)
            # Check for " Delayed on flight" in package note.  Then check if deadline time is EOD.
            # If not, package goes to truck 2.  If so, package goes to truck 3.  Remove from sort list.
            elif "Delayed on flight" in package_.note:
                if package_.deadline_time != "EOD":
                    truck2_load.append(package_.id_)
                    sort_list.remove(package_)
                else:
                    if len(truck3_load) < truck3_.package_max:
                        truck3_load.append(package_.id_)
                        sort_list.remove(package_)
                    else:
                        # Truck 3 could be at max capacity.  If so, append to truck 2.  Remove from sort list.
                        truck2_load.append(package_.id_)
                        sort_list.remove(package_)
            # Package 19 goes with group packages. Remove from sort list.
            elif package_.id_ == 19:
                truck1_load.append(package_.id_)
                sort_list.remove(package_)
            # Early morning goes on truck 1.  Remove from sort list.
            elif "9:00" in package_.note:
                truck1_load.append(package_.id_)
                sort_list.remove(package_)
            # Address update package.  Goes on truck 3.  Remove from sort list.
            elif "Wrong address" in package_.note:
                truck3_load.append(package_.id_)
                sort_list.remove(package_)
            # Morning packages go on truck 1 unless capacity full.  Remove from sort list.
            elif package_.deadline_time != "EOD":
                if len(truck1_load) < truck1_.package_max:
                    truck1_load.append(package_.id_)
                    sort_list.remove(package_)
                else:
                    # if truck 1 full, morning packages appended to truck 2.  Remove from sort list.
                    truck2_load.append(package_.id_)
                    sort_list.remove(package_)
            else:
                # For all other packages, check if truck 3 capacity full.  If not, append to truck 3.
                # Remove from sort list.
                if len(truck3_load) < truck3_.package_max:
                    truck3_load.append(package_.id_)
                    sort_list.remove(package_)
                # If truck 3 full, append to truck 1 unless full.  Remove from sort list.
                elif len(truck1_load) < truck1_.package_max:
                    truck1_load.append(package_.id_)
                    sort_list.remove(package_)
                else:
                    # If all other trucks are full, append to truck 2.  Remove from sort list.
                    truck2_load.append(package_.id_)
                    sort_list.remove(package_)
    # Append truck load lists to trucks
    for load in truck1_load:
        truck1_.package_load.append(load)
    for load in truck2_load:
        truck2_.package_load.append(load)
    for load in truck3_load:
        truck3_.package_load.append(load)


# CSVList instantiation 1
distance_csv = CSVList()
distance_csv.add_list("CSV/DistanceTable.csv")

# CSVList instantiation 2
address_csv = CSVList()
address_csv.add_list("CSV/AddressFile.csv")

# CSVList instantiation 3
package_csv = CSVList()
package_csv.add_list("CSV/PackageFile.csv")

# Creates package HashMap
truck_package_hash = HashMap()

# Call load_package method to insert package objects into HashMap
load_package(package_csv.list, truck_package_hash)

# DeliveryTruck instantiation 1
truck_one = DeliveryTruck.DeliveryTruck(datetime.timedelta(hours=8))

# DeliveryTruck instantiation 2
truck_two = DeliveryTruck.DeliveryTruck(datetime.timedelta(hours=9, minutes=5))

# DeliveryTruck instantiation 3
truck_three = DeliveryTruck.DeliveryTruck(datetime.timedelta(hours=0))

# load_trucks method call for all three trucks
load_trucks(truck_one, truck_two, truck_three, total_packages_list)

# Looks up package with ID 9 from HashMap.
updated_package = truck_package_hash.lookup(9)

# Updates package 9 with new address and class field data
updated_package.set_updated_address("410 S State St", datetime.timedelta(hours=10, minutes=20))

# Inserts updated package 9 back into HashMap
truck_package_hash.insert(9, updated_package)

# Creates address graph instance
address_graph = Graph()

# Adds vertex to address graph for each address stored in CSVList instance
# O(N)time --- O(N)space
for record in address_csv.list:
    vertex = Vertex(record[2])
    address_graph.add_vertex(vertex)

# Records weight of every edge in graph
# O(N^2)time --- O(N)space
for record1 in address_csv.list:
    for record2 in address_csv.list:
        address_graph.add_undirected_edge(record1[2], record2[2],
                                          distance_csv.get_x_y(address_csv.get_csv_id(record1[2]),
                                                               address_csv.get_csv_id(record2[2])))


# Retrieves edge weight from graph
# O(1)time --- O(1)space
def get_graph_distance(location1, location2):
    distance = float(address_graph.edge_weights[(location1, location2)])
    return distance


# Iterates through delivery list to find optimized delivery route.
# Nearest Neighbor Algo
# O(N^2)time --- O(1)space
def iterate_truck_delivery_list(delivery_list, delivery_truck):
    while len(delivery_list) > 0:
        next_distance = float('inf')
        next_parcel = None
        # Updates delivery address if package has not been delivered yet.
        for parcel in delivery_list:
            if parcel.address_update:
                if parcel.address_update_time > delivery_truck.clock:
                    parcel.delivery_success = False
                else:
                    parcel.address = parcel.updated_address
                    parcel.delivery_success = True
            # Retrieves edge weight distance from graph.
            distance = get_graph_distance(delivery_truck.address, parcel.address)
            # Sets next_package and next_distance if lowest distance found
            if distance <= next_distance:
                next_parcel = parcel
                next_distance = distance
        # Updates truck attributes with update_truck method call
        delivery_truck.update_truck(next_parcel.address, next_distance)
        # Updates package attributes with package_delivered method call
        next_parcel.package_delivered(delivery_truck.initial_clock, delivery_truck.clock)
        # Removes next package from delivery list
        delivery_list.remove(next_parcel)
        # Checks package deadline time for successful delivery
        if next_parcel.deadline_time != "EOD":
            if next_parcel.delivery_time > datetime.timedelta(hours=float(next_parcel.deadline_time) * 24):
                next_parcel.delivery_success = False


# Creates delivery list of packages and calls iterate_truck_delivery_list method to sort it
# O(N)time --- O(N)space
def route_delivery(delivery_truck):
    # Looks up truck packages from HashMap and appends them to delivery list
    delivery_list = []
    for id_ in delivery_truck.package_load:
        package = truck_package_hash.lookup(id_)
        delivery_list.append(package)
    # iterate_truck_delivery_list method call
    iterate_truck_delivery_list(delivery_list, delivery_truck)
    # Find distance to home
    home_distance = get_graph_distance(delivery_truck.address, delivery_truck.home)
    # Update truck attributes to head home
    delivery_truck.update_truck(delivery_truck.home, home_distance)


# Routes trucks using route_delivery and truck_driver_ready methods
# O(N^2)time --- O(N)space
def route_trucks(truck1_, truck2_, truck3_):
    route_delivery(truck1_)
    route_delivery(truck2_)
    truck3_.truck_driver_ready(truck1_, truck2_)
    route_delivery(truck3_)


# Route trucks method called on all trucks
route_trucks(truck_one, truck_two, truck_three)


# Displays introduction and truck information to terminal
# O(1)time --- O(1)space
def intro():
    total_truck_mileage = truck_one.miles + truck_two.miles + truck_three.miles
    print("---WGUPS Routing and Delivery---")
    print("Total truck mileage after deliveries: " + str(round(total_truck_mileage, 1)))
    print("Individual truck mileage --- Truck 1: " + str(round(truck_one.miles, 1)) + " --- Truck 2: " +
          str(round(truck_two.miles, 1)) + " --- Truck 3: " + str(round(truck_three.miles, 1)))
    print("Truck departure time --- Truck 1: " + str(truck_one.initial_clock) + " --- Truck 2: " +
          str(truck_two.initial_clock) + " --- Truck 3: " + str(truck_three.initial_clock))
    print("Truck return time --- Truck 1: " + str(truck_one.clock) + " --- Truck 2: " +
          str(truck_two.clock) + " --- Truck 3: " + str(truck_three.clock))
    print("Truck final destination --- Truck 1: " + str(truck_one.address) + " --- Truck 2: " +
          str(truck_two.address) + " --- Truck 3: " + str(truck_three.address))
    print("Truck packages delivered --- Truck 1: " + str(len(truck_one.package_load)) + " --- Truck 2: " +
          str(len(truck_two.package_load)) + " --- Truck 3: " + str(len(truck_three.package_load)))
    print("------------------------")


# Exits program with goodbye message.
# O(1)time --- O(1)space
def goodbye():
    print("Exiting program.  Have a nice day.")
    exit()


# Gives user option to check another package status.
# O(1)time --- O(1)
def repeat_status_check():
    user_input = input("Would you like to check another status?  Enter 1 for yes and 2 for no.")
    if user_input == "1":
        return terminal_display()
    elif user_input == "2":
        return goodbye()
    else:
        print("Invalid entry.")
        return repeat_status_check()


# Retrieves time input from terminal.
# O(1)time --- O(1)space
def get_time_from_user():
    try:
        time = input("To check package/s status, enter time in military HH:MM format (HH = hours, MM = minutes).")
        (h, m) = time.split(":")
        time_to_check = datetime.timedelta(hours=int(h), minutes=int(m))
        return time_to_check
    except ValueError:
        print("Invalid entry.  Please try again.")
        return terminal_display()


# Displays status of specific package to terminal.
# O(1)time --- O(1)space
def status_selection_one(package_time):
    package_id = input("Enter the package ID number.")
    package = truck_package_hash.lookup(int(package_id))
    if package is None:
        print("No record of this package.")
        return repeat_status_check()
    package.display_status_by_time(package_time)
    return repeat_status_check()


# Displays status of all packages to terminal.
# O(N)time --- O(1)space
def status_selection_two(package_time):
    for index in range(1, len(total_packages_list) + 1):
        package = truck_package_hash.lookup(index)
        package.display_status_by_time(package_time)
    return repeat_status_check()


# Retrieves user option decisions and calls method to display appropriate message
# O(1)time --- O(1)space
def terminal_display():
    time = get_time_from_user()
    status_select = input("To see the status of a specific package, enter 1.  To see the status of all packages, "
                          "enter 2.  To exit, enter 3.")
    if status_select == "1":
        status_selection_one(time)
    elif status_select == "2":
        status_selection_two(time)
    elif status_select == "3":
        return goodbye()
    else:
        print("Invalid entry.")
        return repeat_status_check()


# Launches program with intro and terminal_display function calls
class Main:
    intro()
    terminal_display()
