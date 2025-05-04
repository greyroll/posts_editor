from sqlalchemy import create_engine
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, Session, select

from orm_models.category import Category
from orm_models.post import Post
from orm_models.tag import Tag


class DBManager:
	model: SQLModel | None = None

	def __init__(self):
		db_path = "posts.db"
		self.engine = create_engine(f"sqlite:///{db_path}")

	def init_db(self):
		SQLModel.metadata.create_all(self.engine)

	def populate_mock_data(self):
		with Session(self.engine) as session:
			if session.exec(select(Post)).first():
				print("Mock data already exists.")
			else:
				cat1 = Category(name="Technology")
				cat2 = Category(name="Lifestyle")
				tag1 = Tag(name="Python")
				tag2 = Tag(name="FastAPI")
				tag3 = Tag(name="Productivity")
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

	# region Posts

	def get_all_posts(self) -> list[Post]:
		with Session(self.engine) as session:
			return list(session.exec(select(Post).options(selectinload(Post.category), selectinload(Post.tags))).all())

	def get_post_by_id(self, post_id: int) -> Post | None:
		with Session(self.engine) as session:
			return session.exec(select(Post).options(selectinload(Post.category), selectinload(Post.tags)).where(Post.id == post_id)).first()

	def get_posts_by_cat(self, category_name: str) -> list[Post]:
		with Session(self.engine) as session:
			return list(session.exec(select(Post).join(Category).options(selectinload(Post.category), selectinload(Post.tags)).where(Category.name == category_name)).all())

	def get_posts_by_tag(self, tag_name: str) -> list[Post]:
		with Session(self.engine) as session:
			tag = session.exec(select(Tag).options(selectinload(Tag.posts).selectinload(Post.category), selectinload(Tag.posts).selectinload(Post.tags)).where(Tag.name == tag_name)).first()
			return tag.posts

	def create_post(self, title: str, content: str, category_id: int, tag_ids: list[int]) -> Post:
		with Session(self.engine) as session:
			category = self._get_category_by_id(session, category_id)
			if not category:
				raise ValueError("Category not found.")

			tags = []
			for tag_id in tag_ids:
				tag = self._get_tag_by_id(session, tag_id)
				if tag:
					tags.append(tag)
				else:
					raise ValueError(f"Tag with id '{tag_id}' not found.")

			post = Post(title=title, content=content, category_id=category.id, tags=tags)
			session.add(post)
			session.commit()
			session.refresh(post)
			return post

	def update_post(self, post_id: int, title: str, content: str, category_id: int, tag_ids: list[int]) -> Post | None:
		with Session(self.engine) as session:
			post = session.get(Post, post_id)
			if post is None:
				return None

			category = self._get_category_by_id(session, category_id)
			if not category:
				raise ValueError("Category not found.")

			tags = []
			for tag_id in tag_ids:
				tag = self._get_tag_by_id(session, tag_id)
				if tag:
					tags.append(tag)
				else:
					raise ValueError(f"Tag with id '{tag_id}' not found.")

			post.title = title
			post.content = content
			post.category_id = category.id
			post.tags = tags

			session.add(post)
			session.commit()
			session.refresh(post)
			return post

	# endregion

	# region Categories

	def get_all_cats(self) -> list[Category]:
		with Session(self.engine) as session:
			return list(session.exec(select(Category).options(selectinload(Category.posts))).all())

	def get_cat_by_id(self, cat_id: int) -> Category | None:
		with Session(self.engine) as session:
			return session.get(Category, cat_id)

	def _get_category_by_id(self, session: Session, cat_id: int) -> Category | None:
		return session.exec(select(Category).where(Category.id == cat_id)).first()

	def create_cat(self, name: str) -> Category:
		with Session(self.engine) as session:
			cat = Category(name=name)
			session.add(cat)
			session.commit()
			session.refresh(cat)
			return cat

	def update_cat(self, cat_id: int, new_name: str) -> Category:
		with Session(self.engine) as session:
			cat = self._get_category_by_id(session, cat_id)
			if cat is None:
				raise ValueError(f"Category with id '{cat_id}' not found.")
			cat.name = new_name
			session.add(cat)
			session.commit()
			session.refresh(cat)
			return cat

	# endregion

	# region Tags

	def get_all_tags(self) -> list[Tag]:
		with Session(self.engine) as session:
			return list(session.exec(select(Tag).options(selectinload(Tag.posts))).all())

	def create_tag(self, name: str) -> Tag:
		with Session(self.engine) as session:
			tag = Tag(name=name)
			session.add(tag)
			session.commit()
			session.refresh(tag)
			return tag

	def delete_tag(self, tag_id: int):
		with Session(self.engine) as session:
			tag = self._get_tag_by_id(session, tag_id)
			if tag:
				session.delete(tag)
				session.commit()
				return tag
			return None

	# endregion

	# region Private helpers



	def _get_tag_by_id(self, session: Session, tag_id: int) -> Tag | None:
		return session.get(Tag, tag_id)

	# endregion
