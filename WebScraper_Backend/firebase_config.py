import firebase_admin
from firebase_admin import credentials ,auth
import asyncio,os
from fastapi import HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv


load_dotenv()

SERVICE_ACCOUNT_CREDENTIALS = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv('auth_uri'),
    "token_uri": os.getenv('token_uri'),
    "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url'),
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}",
    "universe_domain": "googleapis.com"
}

firebase_database_url = os.getenv("FIREBASE_DATABASE_URL")


try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_CREDENTIALS)
    firebase_admin.initialize_app(cred,{'databaseURL': firebase_database_url})
    print("Firebase Admin SDK initialized successfully!")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")





def verifyFirebaseToken(token:str):
  try:
     decoded_token = auth.verify_id_token(token)
     return decoded_token
  except:
     return HTTPException(status_code=401,detail="Invalid Token")
  
class TokenPayload(BaseModel):
  token:str

async def login(paylod:TokenPayload):
  user = verifyFirebaseToken(paylod.token)
  if isinstance(user, HTTPException):
    raise user
  print("User logged in:", user["email"])
  return {
    "message": "Login successful", 
    "uid": user["uid"], 
    "email": user["email"]
    }

async def signup(payload: TokenPayload):
    user = verifyFirebaseToken(payload.token)
    if isinstance(user, HTTPException):
      raise user
    # Optionally store user info in your DB
    print("User signed up:", user["email"])
    return {
       "message": "Signup successful",
       "uid": user["uid"], 
       "email": user["email"]
       }






async def signup_(data):
 
  email = data.get('email')
  password = data.get('password')

  if not email or not password:
    return {"error": "Email and password are required for signup."}
  
  try:
    # Use keyword arguments for clarity and correctness
    user = auth.create_user(email=email, password=password)
    return {
        "msg": "Successfully Account is Created", 
        "uid": user.uid, 
        "email": user.email
      }
  except Exception as e:
    return {"error":str(e),"data":data}

async def generate_custom_auth_token(data):

  email = data.get('email')
  password = data.get('password') 

  if not email: # Only email is needed to retrieve user
    return {"error": "Email is required to generate a custom token."}
  
  try:
    user = auth.get_user_by_email(email) 

    # Create the custom token
    custom_token_bytes = auth.create_custom_token(user.uid)
    
    return {
        "msg": "Successfully generated custom token for client-side login", 
        "uid": user.uid, 
        "custom_token": custom_token_bytes.decode('utf-8') # Decode bytes to string for JSON
    }
  except auth.AuthError as e:
    # Handle cases like user not found or other authentication errors
    return {"error": f"Failed to generate custom token: {e}", "data": data}
  except Exception as e:
    return {"error": str(e), "data": data}

async def verify_firebase_id_token(id_token: str): 
  if not id_token:
      return {"error": "ID token is required for verification."}

  try:
    # auth.verify_id_token expects the actual Firebase ID Token (JWT string)
    decoded_token = auth.verify_id_token(id_token) 
    uid = decoded_token['uid']
    return {"msg": "Firebase ID Token successfully verified", "uid": uid, "decoded_claims": decoded_token}
  except auth.InvalidIdTokenError:
    return {"error": "Invalid Firebase ID Token. Token is expired, revoked, or malformed."}
  except Exception as e:
    return {"error": str(e)}

# --- Example Usage (Running async functions) ---
async def main_execution_flow():
    # --- 1. Attempting Signup ---
    print("\n--- Attempting verify id token ---")
    verify_firebase_id_token(id_token="VUHZ4fXgN3YHSsIQOwoUJfhOxe53")
    
    
# This ensures that main_execution_flow() runs when the script is executed.
if __name__ == "__main__":
    asyncio.run(main_execution_flow())