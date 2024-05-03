import os
import random
import string
from datetime import datetime

from dotenv import load_dotenv

from app.models import UserInfo, BottleTransaction, UserTransactions, ItemList, Redemption, StaffRedemption, \
    StaffInfo


def generate_code():
    chars_uppercase = string.ascii_uppercase
    chars_digits = string.digits

    # Generate random uppercase letters
    code = ''.join(random.choice(chars_uppercase) for _ in range(3))

    # Generate random digits
    code += ''.join(random.choice(chars_digits) for _ in range(3))

    return code


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


# TODO: implement carousel
# https://developers.line.biz/en/reference/messaging-api/#template-messages

def send_flex_message(user_id, LINE_CHANNEL_ACCESS_TOKEN, requests):
    load_dotenv()
    URL = os.getenv('URL')
    REDIRECT_URI = URL + "/APIs/redeemable?itemID=1&n=1"

    payload = {
        'to': user_id,
        'messages': [
            {
                "type": "flex",
                "altText": "แลกรับรางวัลทันที",
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
                                    "label": "แลกรางวัล",
                                    "uri": REDIRECT_URI
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


def new_transaction(points, machineID, token, db):
    transaction = BottleTransaction(points=points, date=datetime.now(), machineID=machineID, token=token)
    db.add(transaction)
    db.commit()

    # return the transaction ID
    return transaction.bottleTransactionID


def map_user_transaction(userID, bottleTransactionID, db):
    user_transaction = UserTransactions(userID=userID, bottleTransactionID=bottleTransactionID)
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


def get_points_required(itemID, db):
    item = db.query(ItemList).filter(ItemList.itemID == itemID).first()
    return item.pointsRequired


# check if user have the required points to redeem
def redeem(userID, itemID, n, LINE_CHANNEL_ACCESS_TOKEN, requests, db):
    # check if user have enough points to redeem
    user = db.query(UserInfo).filter(UserInfo.userID == userID).first()
    pointsRequired = get_points_required(itemID, db)
    if user.totalPoints < pointsRequired:
        return False

    while True:
        referenceCode = generate_code()
        redemption = db.query(Redemption).filter(Redemption.redemptionID == referenceCode).first()
        if not redemption:
            break
    # deduct n points
    user.totalPoints -= pointsRequired
    # add redemption record
    redemption = Redemption(redemptionID=referenceCode, userID=userID, itemID=itemID, issuedDate=datetime.now(),
                            status='Unused', numberOfItems=n)
    db.add(redemption)
    db.commit()

    # get item name from itemID
    item = db.query(ItemList).filter(ItemList.itemID == redemption.itemID).first()
    name = item.itemName
    # send message to user
    send_message(userID, f"คุณได้รับ 1 {name} - {referenceCode}", LINE_CHANNEL_ACCESS_TOKEN, requests)
    send_message(userID, f"จำนวนขวดสะสมของคุณคงเหลือ {user.totalPoints} ขวด", LINE_CHANNEL_ACCESS_TOKEN, requests)
    return True


# check if token is already used
def check_token(token, db):
    transaction = db.query(BottleTransaction).filter(BottleTransaction.token == token).first()
    if transaction:
        return True
    return False


def new_staff(staffName, location, db):
    staff = StaffInfo(staffName=staffName, location=location)
    db.add(staff)
    db.commit()
    return 'created'


def staff_redemption(staffID, redemptionID, db):
    # check if redemptionID is valid and not redeemed
    redemption = db.query(Redemption).filter(Redemption.redemptionID == redemptionID).first()
    if not redemption:
        return 'invalid redemptionID'
    if redemption.status == 'Redeemed':
        # get the location of the staff
        staff = db.query(StaffInfo).filter(StaffInfo.staffID == staffID).first()
        return f"Redemption {redemptionID} has already been redeemed by {staff.staffName} at {staff.location}"

    staffRedemption = StaffRedemption(redemptionID=redemptionID, staffID=staffID)
    # modify redemption status
    redemption = db.query(Redemption).filter(Redemption.redemptionID == redemptionID).first()
    redemption.status = 'Redeemed'
    redemption.redeemedDate = datetime.now()
    db.add(staffRedemption)
    db.commit()
    return 'created'
