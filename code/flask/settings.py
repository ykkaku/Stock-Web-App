import os

# MONGO_URI = os.environ.get('MONGO_URI')
MONGO_URI = 'mongodb+srv://dsci551:123@cluster0.mhniy.gcp.mongodb.net/news?retryWrites=true&w=majority'


# Google Cloud SQL (MySQL credentials)
PASSWORD = "PApOEaPbJNOM62p1"
PUBLIC_IP_ADDRESS = "35.188.135.112"
LOCAL_ADDRESS = "127.0.0.1"
DBNAME = "stockdb"
PROJECT_ID = "stock-project-294701"
INSTANCE_NAME = "stock-project-294701:us-central1:stock-database"

SECRET_KEY = "yoursecretkey"
SQLALCHEMY_DATABASE_URI = f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = True