from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

# Association table for Contest <-> Problems (Many-to-Many)
contest_problems = Table(
    'contest_problems', Base.metadata,
    Column('contest_id', Integer, ForeignKey('contests.id'), primary_key=True),
    Column('problem_id', Integer, ForeignKey('problems.id'), primary_key=True)
)

# Association table for Contest <-> Users (Many-to-Many)
contest_participants = Table(
    'contest_participants', Base.metadata,
    Column('contest_id', Integer, ForeignKey('contests.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class Contest(Base):
    __tablename__ = "contests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    problems = relationship("Problem", secondary=contest_problems, backref="contests")
    participants = relationship("User", secondary=contest_participants, backref="contests")
