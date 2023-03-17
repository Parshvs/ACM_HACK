import firebase_admin
from firebase_admin import credentials

# Replace the path with the path to your service account key file
cred = credentials.Certificate('E:\6 Sem\ACM\REGISTRATION\REGISTRATION\registration\line-free-c2f74-firebase-adminsdk-qk3hl-ddbc3e621f.json')
firebase_admin.initialize_app(cred)
