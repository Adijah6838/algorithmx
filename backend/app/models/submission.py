import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Language(str, enum.Enum):
    CPP = "C++"
    PYTHON = "Python"
    JAVA = "Java"

class SubmissionStatus(str, enum.Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    WRONG_ANSWER = "Wrong Answer"
    COMPILATION_ERROR = "Compilation Error"
    RUNTIME_ERROR = "Runtime Error"
    TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
    MEMORY_LIMIT_EXCEEDED = "Memory Limit Exceeded"

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    
    language = Column(Enum(Language), nullable=False)
    code = Column(Text, nullable=False)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.PENDING, nullable=False)
    
    execution_time = Column(Float, nullable=True) # in seconds
    memory_used = Column(Float, nullable=True)    # in MB
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    problem = relationship("Problem")
