import os
import random
import database
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Request, HTTPException, Depends
import decryption
from fastapi.responses import RedirectResponse
import requests
from dotenv import load_dotenv
import services

router = APIRouter(
    prefix="/Lotus's_Project",
    tags=['APIs']
)

get_db = database.getDB
decryption = decryption.Decryption()
load_dotenv()

LINE_LOGIN_CHANNEL_ID = os.getenv('LINE_LOGIN_CHANNEL_ID')
LINE_LOGIN_CHANNEL_SECRET = os.getenv('LINE_LOGIN_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI')

global points
global userID
global currentTransactionID


# new bottles transaction
@router.post('/newBottleTransaction', status_code=status.HTTP_201_CREATED)
async def newBottleTransaction(bottleNumber: str, location: str, db: Session = Depends(get_db)):
    global points, currentTransactionID
    # decrypt the number of bottles and store it in num_bottles
    points = decryption.decrypt(bottleNumber)
    # create a new transaction
    currentTransactionID = services.new_transaction(points, location, db)
    # random state number
    STATE = random.randint(1000, 9999)
    # compose line login url
    line_login_url = (
        f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={LINE_LOGIN_CHANNEL_ID}"
        f"&redirect_uri={REDIRECT_URI}&state={STATE}&scope=openid%20profile")
    print(line_login_url)
    return RedirectResponse(line_login_url)


# callback
@router.get('/callback', status_code=status.HTTP_200_OK)
def callback(request: Request, db: Session = Depends(get_db)):
    global userID

    # Get the authorization code from the query string
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
            # check if user already exists, if not, add new user, else, add new transaction
            services.check_user(userID, currentTransactionID, db)
            # send message to user
            services.send_message(userID, f"You have {points} bottles", LINE_CHANNEL_ACCESS_TOKEN, requests)
            # redirect to success page
            return RedirectResponse("/success")
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve user profile")
    else:
        raise HTTPException(status_code=500, detail="Failed to exchange authorization code for access token")


# Login successfully
@router.get('/success', status_code=status.HTTP_200_OK)
async def success():
    return {"message": "Login successfully"}
