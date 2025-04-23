from sqlalchemy import create_engine
from sqlmodel import SQLModel

from orm_models.category import Category
from orm_models.tag import Tag
from orm_models.post_tag import PostTag


class DBManager:
	model: SQLModel | None = None

	def __init__(self):
		db_path =  "./posts.db"
		self.engine = create_engine(f"sqlite:///{db_path}")

	def init_db(self):
		SQLModel.metadata.create_all(self.engine)



db = DBManager()
db.init_db()