import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import mutations
import queries

@strawberry.type
class Query:
    user = queries.resolve_user
    container_list = queries.resolve_container_list
    
@strawberry.type
class Mutation:
    stop_container = mutations.resolve_stop_container
    run_container = mutations.resolve_start_container
    reload_container = mutations.resolve_reload_container
            
schema = strawberry.Schema(query=Query, mutation=Mutation, )
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)