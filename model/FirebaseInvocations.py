"""
This module will be used to make calls to the real-time database.
"""
from firebase import firebase
import json
import pyrebase

# Initialize database
DATABASE = firebase.FirebaseApplication('https://csc207-tli.firebaseio.com/',
                                        None)


def get_current_user(email: str, password: str) -> json:
    """ Return a json object containing database information about the user trying
    to log in.

    :param email: User's email.
    :param password: user's password.
    :return: A json object.
    """
    config = {
        "apiKey": "AIzaSyCkjsbkDtmKUU_77XHDYfNnBZS1E3F82iw",
        "authDomain": "csc207-tli.firebaseapp.com",
        "databaseURL": "https://csc207-tli.firebaseio.com",
        "projectId": "csc207-tli",
        "storageBucket": "csc207-tli.appspot.com",
        "messagingSenderId": "707734809591",
        "appId": "1:707734809591:web:313eb97ac705e6ebb21cf2",
        "measurementId": "G-VQCPWR41LV"
    }
    firebase_db = pyrebase.initialize_app(config)
    auth = firebase_db.auth()
    return auth.sign_in_with_email_and_password(email, password)


def get_user_registration(email: str, password: str) -> json:
    """ Add a new user to Firebase' authentication and return a json object
    containing database information about the new user.

    :param email: User's email
    :param password: User's address.
    :return: A json object.
    """
    config = {
        "apiKey": "AIzaSyCkjsbkDtmKUU_77XHDYfNnBZS1E3F82iw",
        "authDomain": "csc207-tli.firebaseapp.com",
        "databaseURL": "https://csc207-tli.firebaseio.com",
        "projectId": "csc207-tli",
        "storageBucket": "csc207-tli.appspot.com",
        "messagingSenderId": "707734809591",
        "appId": "1:707734809591:web:313eb97ac705e6ebb21cf2",
        "measurementId": "G-VQCPWR41LV"
    }
    firebase_db = pyrebase.initialize_app(config)
    auth = firebase_db.auth()
    return auth.create_user_with_email_and_password(email, password)


def get_user_data(user_type: str, user_id: str) -> json:
    """ Get a user's data base on user_type and user_id.

    :param user_type: Business Owner, CocaCola, Truck Driver
    :param user_id: User's unique id in the database
    :return: a json object containing the user's information
    """
    return DATABASE.get('/' + user_type, user_id)


def get_login_name(user_id: str) -> str:
    """ Return a the name of the user with id user_id.

    :param user_id: User's unique is.
    :return: A string containing a user's name.
    """
    try:
        if DATABASE.get('/Business Owner', user_id):
            user_data = DATABASE.get('/Business Owner', user_id)
            return user_data.get("Name", None)
    except:
        pass
    try:
        if DATABASE.get('/CocaCola', user_id):
            user_data = DATABASE.get('/CocaCola', user_id)
            return user_data.get("Name", None)
    except:
        pass
    try:
        if DATABASE.get('/Truck Driver', user_id):
            user_data = DATABASE.get('/Truck Driver', user_id)
            return user_data.get("Name", None)
    except:
        return ""


def get_list_of_invoice_ids(user_id: str) -> str:
    """ Return a list of a given user's invoices.

    :param user_id: User's unique id.
    :return: a string of invoiceIDs under the userID, where it is separated by commas.
    """
    invoice_ids = ""
    try:
        inventory_db = DATABASE.get('Invoices', user_id)
        for key in inventory_db:
            invoice_ids += str(key) + ','
        return invoice_ids[:-1]
    except:
        return ""


def get_invoice_information(user_id: str, invoice_id: str) -> str:
    """ Return a given invoice's information

    :param user_id: User's unique id.
    :param invoice_id: Invoice's unique id.
    :return: A comma separated string containing the "delivered, issued, paid,
    total price, item, price, quantity" information about an invoice.
    """
    invoice_information = ""
    try:
        inventory_db = DATABASE.get('Invoices', user_id)
        inventory_db = inventory_db.get(invoice_id, None)
        status_db = inventory_db.get("status", None)
        order_db = inventory_db.get("orders", None)[0]
        invoice_information += str(status_db.get("delivered")) + ","
        invoice_information += str(status_db.get("issued")) + ","
        invoice_information += str(status_db.get("paid")) + ","
        invoice_information += str(inventory_db.get("total price")) + ","
        invoice_information += str(order_db.get("item")) + ","
        invoice_information += str(order_db.get("price")) + ","
        invoice_information += str(order_db.get("quantity"))
        return invoice_information
    except:
        return ""

def get_user_information(user_id: str) -> str:
    """

    :param user_id: User's unique id.
    :return: A comma separated string containing the "Address, Email, Name" information about a user
    """
    user_information = ""
    try:
        user_db = DATABASE.get("Business Owner", user_id)
        user_information += str(user_db.get("Address")) + ","
        user_information += str(user_db.get("Email")) + ","
        user_information += str(user_db.get("Name"))
        return user_information
    except:
        return ""

def get_invoice_json(user_id: str, invoice_id: str) -> json:
    """ Return the invoice with id invoice_id as a json object.

    :param user_id: User's unique id.
    :param invoice_id: The invoice's unique id.
    :return: A json object containing the invoice.
    """
    invoice_path = '/Invoices/' + user_id
    return DATABASE.get(invoice_path, invoice_id)


def get_current_invoiceID() -> str:
    """ Get the most recent invoice's id.

    :return: A string containing an invoice's id.
    """
    return DATABASE.get('/Invoices/currentInvoiceID', None)


def increment_current_invoiceID() -> str:
    """ Increment the current invoice's id by 1.

    :param newVal is the new current invoice ID
    :return: None.
    """
    invoiceID = int(DATABASE.get('/Invoices/currentInvoiceID', None))
    invoiceID += 1
    DATABASE.put("/Invoices", "currentInvoiceID", invoiceID)
    return str(invoiceID)


def create_user(address: str, email: str, name: str, password: str, role: str,
                user_id: str) -> None:
    """ Add a new user to the data base.

    :param address: User's address (only applicable to business owners).
    :param email: User's email.
    :param name: User's first and last names.
    :param password: User's password.
    :param role: User's role (Business Owner/Truck Driver/CocaCola).
    :param user_id: User's unique id.
    :return: None.
    """
    if role == "a Business Owner":
        # Add the user to the database.
        DATABASE.put("Business Owner", user_id,
                     {
                         "Address": address,
                         "Email": email,
                         "Name": name,
                         "Password": password
                     })
        # Initialize the user with an invoice.
        items = {"Coke": ["5", "0.45"], "Cherry Coke": ["10", "0.50"]}
        create_invoice(items, user_id, get_current_invoiceID())
    elif role == "a Truck Driver":
        DATABASE.put("Truck Driver", user_id,
                     {
                         "Email": email,
                         "Name": name,
                         "Password": password,
                         "Customers": {}
                     })
    else:
        DATABASE.put(role, user_id,
                     {
                         "Email": email,
                         "Name": name,
                         "Password": password
                     })


def set_invoice_status(user_id: str, invoice_id: str, status_type: str,
                       new_value: bool) -> bool:
    """ Change invoice_id's status based on status_type and new_value.

    :param user_id: Unique id of the user to whom the invoice belongs.
    :param invoice_id: Unique id of the invoice to be changed.
    :param status_type: The status that will be changed.
    :param new_value: The new status' value (either True or False).
    :return: Return True iff the invoice path is in the database.
    """
    invoice_path = '/Invoices/' + user_id + '/' + invoice_id
    if DATABASE.get(invoice_path, '/status'):
        DATABASE.put(invoice_path + '/status', status_type, new_value)
        return True
    return False


def create_invoice(item_dict: dict, user_id: str, invoice_id: str) -> None:
    """ Create a new invoice.

    :param item_dict: key is "item name", value is list like ["5", "4.5"], "5" is quantity and "4.5" is price {"apple": ["5", "4.5"], "banana": ["10", "3.5"]}
    :return: None
    """
    # calculate the total price
    price = 0
    # arrange the order list
    order_list = []
    for item in item_dict:
        # arrange each item info to a small dict
        item_dict_new = {}
        price += int(item_dict[item][0]) * float(item_dict[item][1])
        item_dict_new["item"] = item
        item_dict_new["quantity"] = item_dict[item][0]
        item_dict_new["price"] = item_dict[item][1]
        # append the small dict to the order list
        order_list.append(item_dict_new)
    DATABASE.put("Invoices/" + user_id, invoice_id,
                 {
                     "orders": order_list,
                     'total price': str(round(price, 2)),
                     'status': {
                         'issued': True,
                         'paid': False,
                         'delivered': False
                     }
                 })
    DATABASE.put("Truck Driver/nSTFFgWdZvYpenarvvTmpXxJIYA3/Assigned Invoices",
                 invoice_id, user_id)


# Returns customerID
def get_customers() -> str:
    """ Return all the business owners' unique ids.

    :return: Comma separated string of unique ids.
    """
    customer_ids = ""
    try:
        inventory_db = DATABASE.get('Business Owner', None)
        for key in inventory_db:
            customer_ids += str(key) + ','
        return customer_ids[:-1]
    except:
        return ""


def get_assigned_invoices(user_id: str) -> str:
    """ Return a list of invoices assigne to the user with id user_id.

    :param user_id: Customer's unique id.
    :return: Comma separates string of invoice ids.
    """
    customer_path = '/Truck Driver/' + user_id + '/Assigned Invoices'

    customer_ids = ""
    try:

        inventory_db = DATABASE.get(customer_path, None)
        for key in inventory_db:
            customer_ids += key + ":" + DATABASE.get(customer_path, key) + ","

        return customer_ids[:-1]
    except:
        return ""


if __name__ == '__main__':
    print(get_current_user('testing@gmail.com', 'password'))
