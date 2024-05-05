from typing import ClassVar, Optional

from sqlmodel import create_engine
import sqlalchemy

import warnings


class Engine:
    PATH : ClassVar[str] = "sqlite:///database/main.db"
    ECHO : ClassVar[bool] = False
    
    
    _instance : Optional["Engine"] = None
    
    def __new__(cls, *args, **kwargs) -> "Engine":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    
    def __init__(self):
        self.__engine = create_engine(Engine.PATH, echo=Engine.ECHO)
        
        
    @property
    def engine(self) -> sqlalchemy.Engine:
        return self.__engine
    
    
    
    
    
if __name__ == "__main__":
    warnings.warn("This is a module, not a script. It is not intended to be run directly.")
    
    engine = Engine()
    
    print(engine.engine)
    