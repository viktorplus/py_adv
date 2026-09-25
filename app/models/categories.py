from app.models import db


class Category(db.Model):
    __tablename__ = 'categories'

    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    name: db.Mapped[str] = db.mapped_column(db.String(100), unique=True)

    questions: db.Mapped[list["Question"]] = db.relationship(back_populates="category")

    def __repr__(self):
        return f"<Category {self.id}: {self.name}>"
