class Config:
    SECRET_KEY = '7aLpOS8!Af8baNiuFHnWYb3'
    DATABASE_NAME = 'Plant_Care_DB'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_NAME}'
    LOAD_SAMPLE_DATA = True 
    # True for first-time use