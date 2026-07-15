from sqlalchemy import Column, Integer, String, Boolean
from app.db.postgres import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

from sqlalchemy.dialects.postgresql import JSONB

import enum
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship

class ToolType(str, enum.Enum):
    auth = "auth"
    data = "data"

class ToolMethod(str, enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class Tool(Base):
    __tablename__ = "tools"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    
    type = Column(Enum(ToolType), nullable=False)
    method = Column(Enum(ToolMethod), nullable=False)
    url = Column(String, nullable=False)
    
    cache_ttl_minutes = Column(Integer, default=30)
    auth_tool_id = Column(String, ForeignKey("tools.id"), nullable=True)
    
    headers = Column(JSONB, default={})
    request_params = Column(JSONB, default={})
    response_params = Column(JSONB, default={})
    body_schema = Column(JSONB, default={})
    timeout_seconds = Column(Integer, default=10)
    retries = Column(Integer, default=0)

    auth_tool = relationship("Tool", remote_side=[id])

class Skill(Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    prompt = Column(String, nullable=False)
    category = Column(String)
    tools = Column(JSONB)
    workflow = Column(JSONB, nullable=False)
