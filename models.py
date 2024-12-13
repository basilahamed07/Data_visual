# models.py

from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Time
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import func
from datetime import datetime
from Data_visual.db_config import DATABASE_URL  # Import the database configuration
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)  # Add primary key column
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    test_cases = relationship("TestCase", back_populates="user")
    
    def __repr__(self):
        return f"<User(email={self.email}, role={self.role}, created_at={self.created_at})>"

class TestCase(Base):
    __tablename__ = 'test_cases'
    
    TestCase_id = Column(String(20), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    summary = Column(Text, nullable=True)
    regression = Column(Boolean, default=False)
    new = Column(Boolean, default=False)
    reopen = Column(Boolean, default=False)
    uat = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="test_cases")
    
    @staticmethod
    def generate_test_case_id(session):
        count = session.query(func.count(TestCase.TestCase_id)).scalar()
        next_id = count + 1
        return f"TC_id_{str(next_id).zfill(3)}"

    def __repr__(self):
        return f"<TestCase(TestCase_id={self.TestCase_id}, user_id={self.user_id}, summary={self.summary})>"

class TestExecutionReport(Base):
    __tablename__ = 'test_execution_reports'
    
    id = Column(Integer, primary_key=True)
    model_name = Column(String(255), nullable=False)
    report_id = Column(String(20), ForeignKey('test_cases.TestCase_id'), nullable=False)
    total_testcases = Column(Integer, default=0)
    pass_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)
    no_run = Column(Integer, default=0)
    execution_time = Column(Time, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    report = relationship("TestCase")
    
    def __repr__(self):
        return f"<TestExecutionReport(model_name={self.model_name}, total_testcases={self.total_testcases})>"

# Create engine and session
engine = create_engine(DATABASE_URL)  # Use the imported DATABASE_URL here
Base.metadata.create_all(engine)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


