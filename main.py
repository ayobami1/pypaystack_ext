
"""

Please install pypaystack


"""

import json
import os.path
import random
import string
import uuid
import os
from pprint import pprint

from pypaystack import Transaction, Customer, Plan

"""
All Response objects are a tuple containing status_code, status, message and data

This is the Main script that create Method to seamlessly interact with PyPaystack

With Class Transaction : For Creating and Establishing Transaction both Payable and Receivables

With Class Customer: For Creating Customer Data and also Updating , not really Necessary as Paystack API Automatic create user by email and user ID

With Class Plans: For Creating Plans Subcription 
"""


key = os.getenv('PAYSTACK_API')

def save_user_in_txt(file_name, data):
    with open(file_name, "w") as f:
        f.write(data)

    return True


def read_user_from_txt(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
    return data



def create_plans():
    """
    :return tuple result with three position args, args[0] status code :int, args[1] status : bool, args[2] stautus message :str , args[3] data : json

    :args You are only to initialise these args in the plan create class
     "name": name, : str
     "amount": amount, :int
     "interval": interval,:str (weekly, houly, daily etc check the class intance for more)
     "currency": currency, : str
     "send_sms": send_sms,:bool
     "description": description,:str
     "hosted_page": hosted_page,:bool
     "send_invoices": send_invoices,:bool



    """
    plan = Plan(authorization_key=key)

    # response = plan.create(name="Monthly", amount=1000000, interval="monthly",currency="NGN", description="This is Just Testing Apis",\
    #                        send_sms=True, send_invoices=True, hosted_page=True, hosted_page_url='https://paystack.com/pay/peud1j285n')

    response= plan.getall(10)
    print(response)

"""Manage Customers"""
def manage_customers_profile(email, phone_number, name):

    """
    The Function manage customers it create Fetch and update
    :return:
    """

    """You Should Create Customer First Before making payment"""
    customer = Customer(authorization_key=key)

    """GET user_id from the mail For updating Details"""
    # if  create_customer:
    customer_data = customer.create(email, first_name=name,last_name='', phone=phone_number)
    print(customer_data)
    user_id = customer_data[3].get('id')
    # print(user_id)

    """ We allow force to Creating Cusomer by Using Update this is to ensure we have correct Detials"""

    response = customer.update(email=email, user_id=user_id, first_name=name, last_name="", phone=phone_number) #Add new customer

    print(response)
    # response = customer.getone("CUS_xxxxyy") #Get customer with customer code of  CUS_xxxxyy
    # response = customer.getall() #Get all customers
    #
    #
    # #Instantiate the plan class to manage plans
    #
    # plan = Plan(authorization_key="sk_myauthorizationkeyfromthepaystackguys")
    # response = plan.create("Test Plan", 150000, 'Weekly') #Add new plan
    # response = plan.getone(240) #Get plan with id of 240
    # response = plan.getall() #Get all plans


# create_plans()
#Instantiate the transaction object to handle transactions.
#Pass in your authorization key - if not set as environment variable PAYSTACK_AUTHORIZATION_KEY

def make_transaction():
    """
    We Intantiate this Class methods

    :arg:
        Email str
        phone Number   str
        name str
        This enable us to Create the Customer Before Going ahead to Store


    :return:
    """

    #Instantiate the Class
    transaction = Transaction(authorization_key=key)

    #Create a 16 alphanumeric randome string for unique References
    ref= "".join([random.choice(string.ascii_letters+string.digits) for _ in range(16)])

    email = "sample@gmail.com"
    amount = 200000
    phone_number = '08***********'
    full_name = 'John Doe'
    use_auth = True #  This alow user Permssion  or Autorization if Fasle User will autorize each payment Perform some action when the condition is met and use_auth is False


    """THIS ENDPOINT ALLOW YOU TO GENERATE CHECKOUT LINK AND CHARGE THE CUSTOMER DIRECTLY LIKE A POP UP"""
    path='auto_code.txt'
    print("use_auth value:", use_auth)
    if (not os.path.isfile(path) or os.path.getsize(path) == 0 or not use_auth) :
        # Perform some action when the condition is met and use_auth is False
        # Meaning you always need customer to Autorize each payment
        customer_manager_response = manage_customers_profile(email=email, phone_number=phone_number, name=full_name)
        print('customer_manager_response', customer_manager_response)

        reponse = transaction.initialize(email=email, amount=amount,reference=ref)
        print("Intialiseing Response ",reponse)

        input("Please wait for initialising to complete")
        """THIS ENPOINT ALLOW YOU TO VERIFY IF A USERS AFTER INITIALISE THEM IF YOU DONT WANT TO USE THE ONLINE CHECKOUT"""
        response = transaction.verify(reference=ref)  # Verify a transaction given a reference code "refcode".
        print("Verify response",response)
        response = response[3]

        input("verifying the Referencing to capture the aut code for future Charging !")
        aut_code = response.get('authorization').get("authorization_code")
        print(aut_code)
        #
        # response = transaction.charge(email=email, auth_code=aut_code , amount=amount, metadata={"Dev":"Ayobami","Days":30}) #Charge a customer N100.
        # print(response)
        save_user_in_txt(file_name=path, data=aut_code+'\n'+email)
        # f.write(aut_code+'\n'+email)
        print("aut_code has been saved Sucesfully !")
    else:
        customer_manager_response = manage_customers_profile(email=email, phone_number=phone_number, name=full_name)
        print('customer_manager_response', customer_manager_response)
        data = read_user_from_txt(path)

        auth_code, email = data.split('\n')

        print(auth_code,email, use_auth)

        response = transaction.charge(email=email, auth_code=auth_code, amount=amount,
                                      metadata={"Dev": "Ayobami", "Days": 30})  # Charge a customer N100.
        print(response)

    # response= transaction.fetch_transfer_banks()
    # print(response)
    # #
    # 140938432
    #
    #Instantiate the customer class to manage customers





"""Use this Method to validate account number before trasaction"""
def validate_account_number(account_number=None, bank_code=None):
    import requests
    trasaction = Transaction(authorization_key=key)
    #Set the path to be resolving the Account Number

    if not account_number:
        account_number = '0268639299'

    if not bank_code:
        bank_code = '035A'



    """ We can get the list of Banks and thier code in case before verifying an account number """

    banks = trasaction.fetch_transfer_banks()
    pprint(banks)


    # You can use the Normal Paysatack API endpoint to get the Validation but calling thr Class
    # Handle request which Make HTTP request directly
    url = (f'https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={bank_code}')

    result = trasaction._handle_request(method="GET", data={}, url=url)
    print(result)

   

    # print(response.text)
    # pprint(response_.text)

# validate_account_number()

make_transaction()
