from datetime import datetime

from app.models import Transactions, UserInfo, UserTransactions, Redemption, ItemList


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


def send_flex_message(user_id, LINE_CHANNEL_ACCESS_TOKEN, requests):
    payload = {
        'to': user_id,
        'messages': [
            {
                "type": "flex",
                "altText": "This is a Flex Message",
                "contents": {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://img.freepik.com/free-vector/detailed-point-exchange_23-2148845560.jpg?w=1480"
                               "&t=st=1709981242~exp=1709981842~hmac"
                               "=985a6b4705e20a1c865ae97b173e56419ea3a120ba849f5415fc3203be371ce9",
                        "size": "full",
                        "aspectRatio": "20:13"
                    },
                    "body": {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                            {
                                "type": "text",
                                "text": "สะสม 10 ขวดเพื่อแลกรางวัล",
                                "size": "md",
                                "weight": "regular",
                                "align": "center"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Redeem",
                                    "uri": "http://0.0.0.0:8000/APIs/redeem"
                                },
                                "style": "link"
                            }
                        ]
                    }
                }
            }
        ]
    }

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
    # for item egg only
    if user.totalPoints >= 10:
        # generate redemptionID
        # TODO
        # redemptionRef =
        # deduct 10 points
        user.totalPoints -= 10
        # add redemption record
        redemption = Redemption(userID=userID, itemID=1, date=datetime.now())
        # get item name
        name = db.query(ItemList).filter(ItemList.itemID == 1).first()
        db.add(redemption)
        db.commit()
        # send message to user
        send_message(userID, f"You have redeemed 1 {name}", LINE_CHANNEL_ACCESS_TOKEN, requests)
        send_message(userID, f"You have {user.totalPoints} bottles left", LINE_CHANNEL_ACCESS_TOKEN, requests)
