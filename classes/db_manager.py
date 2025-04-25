from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from orm_models.category import Category
from orm_models.tag import Tag
from orm_models.post_tag import PostTag
from orm_models.post import Post


class DBManager:
	model: SQLModel | None = None

	def __init__(self):
		db_path = "../posts.db"
		self.engine = create_engine(f"sqlite:///{db_path}")

	def init_db(self):
		SQLModel.metadata.create_all(self.engine)


	def populate_mock_data(self):
		with Session(self.engine) as session:
			# Проверим, есть ли уже данные
			if session.exec(select(Post)).first():
				print("Mock data already exists.")
			else:
				# Категории
				cat1 = Category(name="Technology")
				cat2 = Category(name="Lifestyle")

				# Теги
				tag1 = Tag(name="Python")
				tag2 = Tag(name="FastAPI")
				tag3 = Tag(name="Productivity")

				# Посты
				post1 = Post(
					title="Intro to FastAPI",
					content="FastAPI is a modern web framework for building APIs with Python.",
					category=cat1,
					tags=[tag1, tag2]
				)

				post2 = Post(
					title="How to Stay Productive",
					content="Simple techniques to stay focused while working from home.",
					category=cat2,
					tags=[tag3]
				)

				session.add_all([cat1, cat2, tag1, tag2, tag3, post1, post2])
				session.commit()
				print("Mock data added.")



db = DBManager()
db.populate_mock_data()

