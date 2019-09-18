from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Categorie, Item, User


class Database:
    def __init__(self):
        self.engine = create_engine(
            "sqlite:///database.sqlite",
            connect_args={'check_same_thread': False})
        self.Session = sessionmaker(self.engine)
        self.session = self.Session()

    def add_categorie(self, name, description=""):
        self.session.add(Categorie(name, description=description))
        self.session.commit()

    def update_categorie(self, id, name, description):
        categorie = self.get_categorie(id)
        categorie.name = name
        categorie.description = description
        self.session.add(categorie)
        self.session.commit()

    def get_categories(self):
        return self.session.query(Categorie).all()

    def get_categorie(self, id=0):
        return self.session.query(Categorie).get(id)

    def delete_categorie(self, id):
        self.session.delete(self.get_categorie(id))
        self.session.commit()

    def add_item(self, user_id, cat_id, name, description):
        self.session.add(Item(user_id, cat_id, name, description))
        self.session.commit()

    def update_item(self, id, name, description):
        item = self.get_item(id)
        item.name = name
        item.description = description
        self.session.add(item)
        self.session.commit()

    def get_item(self, id):
        return self.session.query(Item).get(id)

    def delete_item(self, id):
        self.session.delete(self.get_item(id))
        self.session.commit()

    def add_user(self, name, email, password_hash):
        self.session.add(User(name, email, password_hash))
        self.session.commit()

    def check_credentials(self, email, password_hash):
        return self.session.query(User).filter(
            User.email == email
        ).filter(
            User.password_hash == password_hash
        ).first()

    def get_user(self, user_id):
        return self.session.query(User).get(user_id)

    def get_user_by_login(self, user_login):
        return self.session.query(User).filter(User.name == user_login).first()


db = Database()
