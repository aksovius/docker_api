import strawberry

    
@strawberry.type
class Container:
    id: str
    name: str
    status: str
    index: str