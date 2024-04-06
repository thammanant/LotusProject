import os
import random
from pathlib import Path

from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
import requests
from dotenv import load_dotenv
from starlette.responses import HTMLResponse

from app import services
from app.database import getDB
from app.decryption import Decryption

router = APIRouter(
    prefix="/APIs",
    tags=['APIs']
)

get_db = getDB
decryption = Decryption()
load_dotenv()

LINE_LOGIN_CHANNEL_ID = os.getenv('LINE_LOGIN_CHANNEL_ID')
LINE_LOGIN_CHANNEL_SECRET = os.getenv('LINE_LOGIN_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI')

global points
global userID
global currentTransactionID


# new bottles transaction
@router.get('/newBottleTransaction', status_code=status.HTTP_200_OK)
async def newBottleTransaction(data: str, db: Session = Depends(get_db)):
    global points, currentTransactionID
    # decrypt the number of bottles and store it in num_bottles
    all_data = decryption.decrypt(data)
    points = all_data.get('points')
    location = all_data.get('location')
    token = str(all_data.get('iat'))
    # check if token is already used
    if services.check_token(token, db):
        html_content = Path('app/invalidToken.html').read_text()
        return HTMLResponse(content=html_content, status_code=200)

    # create a new transaction
    currentTransactionID = services.new_transaction(points, location, token, db)
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
    global userID, points

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
            services.check_user(userID, currentTransactionID, points, db)
            # get total points
            totalPoints = services.get_all_points(userID, db)
            # send message to user
            services.send_message(userID, f"จำนวนขวดเพิ่ม {points} ขวด - จำนวนขวดทั้งหมดของคุณมี {totalPoints} ขวด",
                                  LINE_CHANNEL_ACCESS_TOKEN, requests)
            # check if user can redeem
            if totalPoints >= 10:
                # send message to user
                services.send_flex_message(userID, LINE_CHANNEL_ACCESS_TOKEN, requests)
            # redirect to success page
            return RedirectResponse("/APIs/success")
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve user profile")
    else:
        raise HTTPException(status_code=500, detail="Failed to exchange authorization code for access token")


# Login successfully
@router.get('/success', status_code=status.HTTP_200_OK)
async def success():
    html_content = Path('app/Login.html').read_text()
    return HTMLResponse(content=html_content, status_code=200)


# Redeem successfully
@router.get('/redeemable', status_code=status.HTTP_200_OK)
async def redeem(db: Session = Depends(get_db)):
    # check if user have enough points to redeem
    user = db.query(services.UserInfo).filter(services.UserInfo.userID == userID).first()
    if user.totalPoints >= 10:
        services.redeem(userID, LINE_CHANNEL_ACCESS_TOKEN, requests, db)
        html_content = Path('app/Redeemed.html').read_text()
        return HTMLResponse(content=html_content, status_code=200)
    else:
        html_content = Path('app/NotEnoughPoints.html').read_text()
        return HTMLResponse(content=html_content, status_code=200)


# Clear all data
@router.get('/clear', status_code=status.HTTP_200_OK)
async def clear(db: Session = Depends(get_db)):
    services.clear(db)
    return 'cleared'


# Show all data in tables format
@router.get('/show', status_code=status.HTTP_200_OK)
async def show(db: Session = Depends(get_db)):
    return services.show_all(db)
