import numpy as np
from tabulate import tabulate
from resources.lib import meli


conn = meli.Meli(client_id=280693783442951, client_secret="gdXsD4Tkouusjo7X7cpLTChZ8cHUDQiL")

current_accesstoken = 'ACCESS_TOKEN'



def get_userID(access_token=None):

    try:
        params = {'access_token': access_token}

        response = conn.get(path="/users/me", params=params).json()

        userID = response['id']

        return userID
    except ConnectionError:
        print('error getting user')


def get_items(UID, accesstoken, offset=0):

    query = '/users/{Cust_id}/items/search'

    url = query.replace('{Cust_id}', str(UID))

    params = {'access_token': accesstoken,'limit':100,'offset':offset}

    response = conn.get(path=url, params=params).json()

    return response['results']

def get_item_quantity(UID, accesstoken):

    query = '/users/{Cust_id}/items/search'

    url = query.replace('{Cust_id}', str(UID))

    params = {'access_token': accesstoken}

    response = conn.get(path=url, params=params).json()

    if response['paging']['total'] is not None:
        return response['paging']['total']


def get_itemsbyID(item_id,accesstoken):

    query='/items/{Item_id}'

    url = query.replace('{Item_id}', str(item_id))

    params = {'access_token': accesstoken}

    response = conn.get(path=url, params=params).json()

    return response


def change_item_price(item_id,accesstoken,price):

    query = '/items/{Item_id}'

    url = query.replace('{Item_id}', str(item_id))

    params = {'access_token': accesstoken}

    body = {
        'price':price
    }

    response = conn.put(path=url, params=params,body=body).json()

    return response

def change_item_description(item_id,accesstoken,description):

    query = '/items/{Item_id}/description'

    url = query.replace('{Item_id}', str(item_id))

    params = {'access_token': accesstoken}

    body = {
        "plain_text": description
    }

    response = conn.put(path=url, params=params,body=body).json()

    return response


def PercentRefactor_itemsbyList(UID,itemID_list,percent,accesstoken):
    for items in itemID_list:
        x = get_itemsbyID(items, accesstoken)
        table = []
        table.append(['Item ID:', x['id']])
        table.append(['Title:', x['title']])
        table.append(['Price:', x['price']])
        table.append(['Permalink:', x['permalink']])
        with open("description.txt", "r") as myfile:
            data = myfile.read()

        current_price = x['price']
        priceraise = (current_price * percent) / 100
        refaction_price = current_price + priceraise
        pricedata = data.replace('{precio}', str(refaction_price))
        titledata = pricedata.replace('{title}', x['title'])
        print(tabulate(table))
        print('Changing price ', x['price'], ' to ', refaction_price)
        # change_item_price(item_id, accesstoken, price)
        # change_item_description(item_id, accesstoken, titledata)
        print('Refactor Completed.')



def refactor_item(UID,item_id,accesstoken,price):

    x = get_itemsbyID(item_id,accesstoken)
    table = []
    table.append(['Item ID:',x['id']])
    table.append(['Title:', x['title']])
    table.append(['Price:', x['price']])
    table.append(['Permalink:',x['permalink']])
    with open("description.txt", "r") as myfile:
        data = myfile.read()
    pricedata = data.replace('{precio}',price)
    titledata = pricedata.replace('{title}',x['title'])
    print(tabulate(table))
    print('Changing price ',x['price'],' to ',price)
    change_item_price(item_id,accesstoken,price)
    change_item_description(item_id,accesstoken,titledata)
    print('Refactor Completed.')


def PercentRefactor_allitems(UID,percent,accesstoken):
    total = get_item_quantity(UID,accesstoken)
    x = str(total)
    y = x[0]
    pagination = int(total/int(y))
    offset = 0
    query = 1
    for page in range(0,pagination):
        itemID_list = get_items(UID,accesstoken,offset)
        offset = offset+100
        for items in itemID_list:
            x = get_itemsbyID(items, accesstoken)
            table = []
            table.append(['Title:', x['title']])
            table.append(['Price:', x['price']])
            with open("/home/neib/Documents/Melchior-dev/core/description.txt", "r") as myfile:
                data = myfile.read()

            current_price = x['price']
            priceraise = (current_price * percent) / 100
            refaction_price = current_price + priceraise
            pricedata = data.replace('{precio}', str(refaction_price))
            titledata = pricedata.replace('{title}', x['title'])
            #print(tabulate(table))
            #print('Query Item: ', query)
            #print('Changing price ', x['price'], ' to ', refaction_price)
            # change_item_price(item_id, accesstoken, price)
            # change_item_description(item_id, accesstoken, titledata)
            #print('Refactor Completed.')

            if query == total:
                print('All Items refacted')
                return None

            query= query+1

