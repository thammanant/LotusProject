from datetime import datetime
from models import UserInfo, Transactions, UserTransactions, Redemption


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


def add_points(userID, points, db):
    user = db.query(UserInfo).filter(UserInfo.userID == userID).first()
    user.totalPoints += int(points)
    db.commit()
    return 'created'


def get_all_points(userID, db):
    user = db.query(UserInfo).filter(UserInfo.userID == userID).first()
    return user.totalPoints


# check if user already exists, if not, add new user, else, add new transaction
def check_user(userID, transactionID, points, db):
    user = db.query(UserInfo).filter(UserInfo.userID == userID).first()
    if not user:
        add_new_user(userID, db)
        map_user_transaction(userID, transactionID, db)

    else:
        map_user_transaction(userID, transactionID, db)

    add_points(userID, points, db)
    return 'created'


# check if user have the required points to redeem
def redeemable(userID, LINE_CHANNEL_ACCESS_TOKEN, requests, db):
    user = db.query(UserInfo).filter(UserInfo.userID == userID).first()
    if user.totalPoints >= 10:
        # generate redemptionID
        redemptionRef = db.query(Redemption).count() + 1
        # deduct 10 points
        user.totalPoints -= 10
        # add redemption record
        redemption = Redemption(redemptionID=redemptionRef,userID=userID, itemID=1, date=datetime.now())
        db.add(redemption)
        db.commit()
        # send message to user
        send_message(userID, f"You have redeemed 1 item", LINE_CHANNEL_ACCESS_TOKEN, requests)
        return True
    else:
        send_message(userID, f"You do not have enough points to redeem", LINE_CHANNEL_ACCESS_TOKEN, requests)
        return False
