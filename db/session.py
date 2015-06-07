from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql+pymysql://chat_room:room_chat@localhost/chat_room', echo=True)
Session = sessionmaker(bind=engine)