import strawberry
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from strawberry.asgi import GraphQL
import mutations
import queries
from fastapi.responses import HTMLResponse
from typing import List
import asyncio
import docker
from nvitop import MigDevice
import json

client = docker.from_env()
mig = MigDevice.all()
@strawberry.type
class Query:
    container_status = queries.resolve_status_list
@strawberry.type
class Mutation:
    stop_container = mutations.resolve_stop_container
    start_container = mutations.resolve_start_container
    reload_container = mutations.resolve_reload_container
    stop_all_containers = mutations.resolve_stop_all_container
    start_containers = mutations.resolve_start_containers
            
schema = strawberry.Schema(query=Query, mutation=Mutation, )
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)

# @app.websocket("/graphql/wss")
# async def websocket_endpoint(websocket: WebSocket):
#     sender = websocket.cookies.get("X-Authorization")
#     export = Exporter()
#     print('Auth:', sender)
    # if sender:
    #     await websocket.accept()
    #     try:
    #         for i in range(60):
    #             #export.start()
    #             #await websocket.send_text(json.dumps(queries.get_containers(ws=True)))
    #             print((60 - i)*5, 'sec left')
    #             try:
    #                 await asyncio.sleep(5)
    #             except asyncio.CancelledError:
    #                 print("CancelledError")
    #     except WebSocketDisconnect:
            
    #         print('disconnected')
