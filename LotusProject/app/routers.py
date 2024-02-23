import os
import database
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Request, HTTPException, Depends
import decryption
from fastapi.responses import RedirectResponse
import requests

router = APIRouter(
    prefix="/Lotus's_Project",
    tags=['APIs']
)

get_db = database.getDB
decryption = decryption.Decryption()
# LINE Login settings
LINE_LOGIN_CHANNEL_ID = os.getenv('LINE_LOGIN_CHANNEL_ID')
LINE_LOGIN_CHANNEL_SECRET = os.getenv('LINE_LOGIN_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI')
STATE = 12345
# bottle info
global num_bottles
# userID
global userID


def send_message(user_id, message):
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


# new bottles transaction
@router.post('/newBottleTransaction', status_code=status.HTTP_201_CREATED)
async def newBottleTransaction(bottleNumber: str, db: Session = Depends(get_db)):
    global num_bottles
    num_bottles = decryption.decrypt(bottleNumber)
    line_login_url = (
        f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={LINE_LOGIN_CHANNEL_ID}"
        f"&redirect_uri={REDIRECT_URI}&state=12345&scope=openid%20profile")
    # change state TODO
    print(line_login_url)
    return RedirectResponse(line_login_url)


# callback
@router.get('/callback', status_code=status.HTTP_200_OK)
async def callback(request: Request):
    global userID  # Consider avoiding global variables if possible

    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": LINE_LOGIN_CHANNEL_ID,
        "client_secret": LINE_LOGIN_CHANNEL_SECRET,
    }

    token_url = "https://api.line.me/oauth2/v2.1/token"
    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        user_profile_url = "https://api.line.me/v2/profile"
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = requests.get(user_profile_url, headers=headers)

        if profile_response.status_code == 200:
            userID = profile_response.json()["userId"]
            await send_message(userID, "Hello, World!")  # Assuming send_message is async
            return RedirectResponse("/success")
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve user profile")
    else:
        raise HTTPException(status_code=500, detail="Failed to exchange authorization code for access token")


# Login successfully
@router.get('/success', status_code=status.HTTP_200_OK)
async def success():
    return {"message": "Login successfully"}
