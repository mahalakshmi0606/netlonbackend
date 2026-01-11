import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root123@localhost/billing'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '114c9d0510be3c3b856ead1a7d8856be00b21b5b5486c6aadcd1b1746b98cac6'
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # This will create an absolute path to your uploads folder in your current working directory
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx', 'xlsx'}  # Includes pdf which is good if you want to allow pdf uploads
   
    