import strawberry

    
@strawberry.type
class Container:
    id: str
    status: str
    name: str

@strawberry.input
class ContainerInput:
    name: str
    port: int
    gpu: int
    device: int
    userDir: str
    