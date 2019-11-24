"""
This module will be used to make calls to the real-time database.
"""
from flask import Request, Flask
from firebase import firebase
# Initialize database
DATABASE = firebase.FirebaseApplication('https://csc207-tli.firebaseio.com/',
                                        None)


def get_user_data(user_type: str, user_id: str):
    """ Get a user's data base on user_type and user_id.

    :param user_type: Business Owner, CocaCola, Truck Driver
    :param user_id: User's unique id in the database
    :return: a json object containing the user's information
    """
    return DATABASE.get('/' + user_type, user_id)


def get_login_name(userID):
    """ Get a user's data base on user_type and user_id.

    :param user_type: Business Owner, CocaCola, Truck Driver
    :param user_id: User's unique id in the database
    :return: a json object containing the user's information
    """
    try:
        if (DATABASE.get('/Business Owner', userID) != None):
            userDATA = DATABASE.get('/Business Owner', userID)
            return userDATA.get("Name", None)
    except:
        pass
    try:
        if (DATABASE.get('/CocaCola', userID) != None):
            userDATA = DATABASE.get('/CocaCola', userID)
            return userDATA.get("Name", None)
    except:
        pass
    try:
        if (DATABASE.get('/Truck Driver', userID) != None):
            userDATA = DATABASE.get('/Truck Driver', userID)
            return userDATA.get("Name", None)
    except:
        return ""

def get_list_of_invoice_ids(userID):
    """
    :param userID: the userId
    :return: a string of invoiceIDs under the userID, where it is separated by commas and the last number will be
    the total number of invoices
    """
    listOfInvoiceIDs = ""
    userDATA = DATABASE.get('/Business Owner', userID)
    inventorydb = userDATA.get("Invoices")
    totalInvoices = 0
    for key in inventorydb:
        listOfInvoiceIDs+=key + ','
        totalInvoices += 1
    return listOfInvoiceIDs + totalInvoices