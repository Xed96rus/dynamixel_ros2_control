from pydantic import BaseModel
from typing import List

class ResponseModel(BaseModel):
    status: str
    reason: str = None

class RequestModel(BaseModel):
    joint_names: List[str]
    positions: List[float]
