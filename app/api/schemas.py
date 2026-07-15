from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    firstname: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    firstname: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ToolEndpoint(BaseModel):
    method: str
    url: str
    timeout: Optional[int] = None
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    response: Optional[Dict[str, str]] = None

class TokenCache(BaseModel):
    enabled: bool
    key: str
    ttl_field: str

class TokenEndpoint(BaseModel):
    strategy: str
    endpoint: Optional[ToolEndpoint] = None
    cache: Optional[TokenCache] = None

class ToolAuthentication(BaseModel):
    type: str
    token: Optional[TokenEndpoint] = None

class ToolInput(BaseModel):
    source: str
    type: str
    required: bool

class ErrorResponse(BaseModel):
    status: int
    code: str

class SuccessResponse(BaseModel):
    status_codes: List[int]
    fields: Dict[str, Dict[str, str]]

class ToolResponse(BaseModel):
    success: Optional[SuccessResponse] = None
    errors: Optional[List[ErrorResponse]] = None

class ToolCreate(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    version: str
    tags: Optional[List[str]] = None
    endpoint: Optional[ToolEndpoint] = None
    authentication: Optional[ToolAuthentication] = None
    headers: Optional[Dict[str, str]] = None
    inputs: Optional[Dict[str, ToolInput]] = None
    response: Optional[ToolResponse] = None

class ToolResponseModel(ToolCreate):
    class Config:
        from_attributes = True

class ToolParameter(BaseModel):
    type: str
    required: bool

class ToolAuthenticationDef(BaseModel):
    type: str

class APIToolCreate(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    type: str
    method: str
    url: str
    
    cache_ttl_minutes: Optional[int] = 30
    auth_tool_id: Optional[str] = None
    
    headers: Optional[Dict[str, str]] = {}
    request_params: Optional[Dict[str, str]] = {}
    response_params: Optional[Dict[str, str]] = {}
    body_schema: Optional[Dict[str, Any]] = {}
    timeout_seconds: Optional[int] = 10
    retries: Optional[int] = 0

class WorkflowStep(BaseModel):
    tools: Optional[List[str]] = None
    next: Optional[List[str]] = None

class WorkflowDef(BaseModel):
    required: Optional[List[str]] = None
    steps: Dict[str, WorkflowStep]

class SkillCreate(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    prompt: str
    category: Optional[str] = None
    tools: Optional[List[Any]] = None
    workflow: WorkflowDef
