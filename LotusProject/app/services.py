from datetime import datetime
from models import UserInfo, Transactions, UserTransactions


def send_message(user_id, message, LINE_CHANNEL_ACCESS_TOKEN, requests):
    # Construct the request payload
    payload = {
        'to': user_id,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }

    # Send the request to the LINE Messaging API
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print("Failed to send message:", response.json())


def add_new_user(userID, db):
    user = UserInfo(userID=userID, accountType='LINE', totalPoints=0)
    db.add(user)
    db.commit()
    return 'created'


def new_transaction(points, location, db):
    transaction = Transactions(points=points, date=datetime.now(),
                               location=location)
    db.add(transaction)
    db.commit()

    # return the transaction ID
    return transaction.transactionID


def map_user_transaction(userID, transactionID, db):
    user_transaction = UserTransactions(userID=userID, transactionID=transactionID)
    db.add(user_transaction)
    db.commit()
    return 'created'


# check if user already exists, if not, add new user, else, add new transaction
def check_user(userID, transactionID, db):
    user = db.query(UserInfo).filter(UserInfo.userID == userID).first()
    if not user:
        add_new_user(userID, db)
    else:
        map_user_transaction(userID, transactionID, db)

    return 'created'
