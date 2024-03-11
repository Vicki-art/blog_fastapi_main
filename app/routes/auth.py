from fastapi import  Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from .. import schemas, models, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session



router = APIRouter(tags = ["Authentication"])

@router.post("/login", response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    logged_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not logged_user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")

    if not utils.verify(user_credentials.password, logged_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_token(data = {"user_id": logged_user.id})

    return JSONResponse(content = {"token": access_token, "token_type": "bearer"})


