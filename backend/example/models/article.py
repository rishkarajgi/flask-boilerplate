from backend.database import (
    Column,
    DateTime,
    Model,
    String,
    Text,
    association_proxy,
    db,
    foreign_key,
    relationship,
    slugify,
)
from backend.utils.date import utcnow


@slugify('title')
class Article(Model):
    title = Column(String(100))
    slug = Column(String(100))
    publish_date = Column(DateTime)
    last_updated = Column(DateTime, nullable=True)
    file_path = Column(String(255), nullable=True)
    header_image = Column(String(255), nullable=True)
    preview = Column(Text)
    html = Column(Text)

    category_id = foreign_key('Category', nullable=True)
    category = relationship('Category', back_populates='articles')

    __repr_props__ = ('id', 'title')

    @classmethod
    def get_published(cls):
        return cls.query\
            .filter(cls.publish_date <= utcnow())\
            .order_by(cls.publish_date.desc(), cls.last_updated.desc())\
            .all()
