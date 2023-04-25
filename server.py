import strawberry
from fastapi import FastAPI, UploadFile, File
from strawberry.asgi import GraphQL
import mutations
import queries
from utils import *
from typing import List, Optional

DATA_DIR = '/home/gil/Desktop/class_files'

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


@app.get('/file')
async def result_endpoint(folder: str, filename: str):
  
    path = os.path.join(DATA_DIR, folder, filename)
    
    # check if result folder exist
    if os.path.isfile(path):
        return FileResponse(path=path, filename=filename) 
    # if file not found, return status
    else:
        return {"status": 'Not found'}
           
@app.post('/file')
async def file_upload_endpoint(folder: Optional[str] ="temp", 
                              file: List[UploadFile] = File(...)):
    print(folder)
    
    upload_dir = os.path.join(DATA_DIR, folder)
    await upload_file(file, upload_dir)
    return {"success": 1}

# upload 1 image for pages
@app.post('/image')
async def image_upload_endpoint(folder: Optional[str] ="temp", 
                              image: UploadFile = File(...)):
    
    print(folder)
    print(image)
    upload_dir = os.path.join(DATA_DIR, folder)
    await upload_one_file(image, upload_dir)
    return {"success": 1, "file": {"url": f"https://210.102.178.108.nip.io/resource/file?folder={folder}&filename={image.filename}"}}
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
