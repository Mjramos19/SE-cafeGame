from constants import *

class Table(GameObject):
    """
    A furniture object that holds Seat objects.
    
    Attributes:
        seats (list): The list of individual Seat objects associated with this table.
        open (bool): Whether the table has available seats.
    """
    def __init__(self, x, y, w=70, h=40, color=TABLE_COLOR, seats = []):
        super().__init__(x, y, w, h, color)
        self.open = True
        self.seats = seats
        self.open = True

class Seat(GameObject):
    """
    A specific seating spot for a customer.
    
    Attributes:
        state (str): Current occupancy status (open, reserved, taken).
        seatedCustomer (Customer): The customer assigned to this seat.
        num (int): The unique seat ID for orientation and identification.
    """
    def __init__(self, x, y, num, w=70, h=15, color=SEAT_COLOR):
        super().__init__(x, y, w, h, color)
        self.state = "open"
        self.seatedCustomer = None
        self.num = num

    def get_seatX(self):
        """Returns the horizontal position of the seat."""
        return self.rect.x

    def get_seatY(self):
        """Returns the vertical position of the seat."""
        return self.rect.y

    def reserveSeat(self, customer):
        """Sets seat state to reserved for a specific customer."""
        self.state = "reserved"
        self.seatedCustomer = customer

    def occupySeat(self, customer):
        """Sets seat state to taken by a specific customer."""
        self.state = "taken"
        self.seatedCustomer = customer

    def openSeat(self):
        """Resets the seat to an open state."""
        self.state = "open"
        self.seatedCustomer = None
