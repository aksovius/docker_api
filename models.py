import strawberry

    
@strawberry.type
class Container:
    index: int
    id: str
    name: str
    status: str
    gpu: int
    device: int
    total: str
    free: str
    used: str
