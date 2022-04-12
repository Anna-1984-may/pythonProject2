from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///projects.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
"""
class ProjectName(Base):
    __tablename__ = 'names'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tags = relationship("ProjectTag", cascade="all,delete", back_populates='name')

    def __str__(self):
        return self.name
    
    @classmethod
    def add(cls, name):
        name = cls(name=name)
        session.add(name)
        session.commit()
        return name
"""

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tags = relationship("Tag", cascade="all,delete", back_populates="project")

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, name):
        project = cls(name=name)
        session.add(project)
        session.commit()
        return project

"""

class ProjectTag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False)
    name_id = Column(Integer, ForeignKey('names.id'))
    name = relationship("ProjectName", back_populates="tags")

    def __str__(self):
        return self.tag 
    
    @classmethod
    def add(cls, tag, name):
        tag = cls(tag=tag, name=name)
        session.add(tag)
        session.commit()
        return tag
"""

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tags")

    def __str__(self):
        return self.tag

    @classmethod
    def add(cls, tag, project):
        tag = cls(tag=tag, project=project)
        session.add(tag)
        session.commit()
        return tag

Base.metadata.create_all(engine)