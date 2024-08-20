from pydantic import BaseModel

class UserRoleResponse(BaseModel):
    id:int
    name:str
    description:str
    
    class Config:
        orm_mode = True
        from_attributes=True