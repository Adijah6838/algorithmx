import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base

class Difficulty(str, enum.Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXPERT = "Expert"

class Category(str, enum.Enum):
    ARRAYS = "Arrays"
    STRINGS = "Strings"
    DYNAMIC_PROGRAMMING = "Dynamic Programming"
    GRAPH_THEORY = "Graph Theory"
    SORTING_SEARCHING = "Sorting and Searching"
    NUMBER_THEORY = "Number Theory"
    GREEDY = "Greedy Algorithms"
    TREES = "Trees"

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    input_spec = Column(Text, nullable=False)
    output_spec = Column(Text, nullable=False)
    constraints = Column(Text, nullable=True)
    
    difficulty = Column(Enum(Difficulty), default=Difficulty.EASY, nullable=False)
    category = Column(Enum(Category), default=Category.ARRAYS, nullable=False)
    is_published = Column(Boolean, default=False)
    
    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_sample = Column(Boolean, default=False)

    problem = relationship("Problem", back_populates="test_cases")
