import datetime


# Blueprint for Package objects.
# O(1)time --- O(N)space
class Package:
    def __init__(self, id_, address, city, state, zipcode, deadline_time, weight, note):
        self.id_ = id_
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.note = note
        self.status = "at the hub"
        self.departure_time = None
        self.delivery_time = None
        self.address_update = False
        self.address_update_time = None
        self.updated_address = None
        self.old_address = None
        self.delivery_success = True

    # Sets updated address data fields
    # O(1)time --- O(1)space
    def set_updated_address(self, new_address, update_time):
        self.address_update = True
        self.updated_address = new_address
        self.old_address = self.address
        self.address_update_time = update_time

    # Checks status of package at specific time and print_package_details and delivery_check methods.
    # O(1)time --- O(1)space
    def display_status_by_time(self, time):
        # Finds status of package at terminal input time
        if self.delivery_time <= time:
            package_status = "delivered"
        elif self.departure_time <= time:
            package_status = "en route"
        else:
            package_status = "at the hub"
        # Checks for address update.  If not, print_package_details and delivery_check method called.
        if self.address_update:
            # If address update time is greater than terminal input time, address update is not reflected in message.
            # If less than, address update is reflected in message.
            if self.address_update_time > time:
                print(f'Package {str(self.id_)} status at {str(time)}: {package_status}')
                print(f'Departure time: {str(self.departure_time)} Delivery time: {str(self.delivery_time)}')
                # Check for string or datetime in deadline_time field
                if self.deadline_time != "EOD":
                    print(f'Deadline time: {datetime.timedelta(hours=float(self.deadline_time) * 24)}')
                else:
                    print(f'Deadline time: {self.deadline_time}')
                print(f'{self.old_address}, {self.city}, {self.zipcode}')
                print(f'Weight: {self.weight}')
                self.delivery_check(package_status)
            else:
                self.print_package_details(time, package_status)
                self.delivery_check(package_status)
        else:
            self.print_package_details(time, package_status)
            self.delivery_check(package_status)

    # Updates status of package upon delivery
    # O(1)time --- O(1)space
    def package_delivered(self, departure_time, delivery_time):
        self.departure_time = departure_time
        self.delivery_time = delivery_time

    # Prints package details.  Checks if deadline_time field is string or datetime for appropriate data type display.
    # O(1) time --- O(1)space
    def print_package_details(self, time, package_status):
        print(f'Package {str(self.id_)} status at {str(time)}: {package_status}')
        print(f'Departure time: {str(self.departure_time)} Delivery time: {str(self.delivery_time)}')
        if self.deadline_time != "EOD":
            print(f'Deadline time: {datetime.timedelta(hours=float(self.deadline_time) * 24)}')
        else:
            print(f'Deadline time: {self.deadline_time}')
        print(f'{self.address}, {self.city}, {self.zipcode}')
        print(f'Weight: {self.weight}')

    # Checks delivery status and displays message.
    # O(1)time --- O(1)space
    def delivery_check(self, package_status):
        if package_status == "delivered":
            if not self.delivery_success:
                print("Delivery unsuccessful")
                print('---------------------------------')
            else:
                print("Delivery successful")
                print('---------------------------------')
        else:
            print('---------------------------------')
