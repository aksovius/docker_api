import strawberry

@strawberry.type
class User:
    name: str
    age: int
    
@strawberry.type
class Container:
    id: str
    name: str
    status: str
    image: str
