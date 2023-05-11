import strawberry
from fastapi import FastAPI,  UploadFile, File
from strawberry.asgi import GraphQL
import mutations
#import queries
from middleware import AuthorizationMiddleware
from utils import *
from typing import List, Optional
from config import DATA_DIR
from fastapi.responses import  FileResponse

@strawberry.type
class Query:
    #container_status = queries.resolve_status_list
    @strawberry.field
    def _dummy(self) -> Optional[str]:
        return None
@strawberry.type
class Mutation:
    stop_container = mutations.resolve_stop_container
    start_container = mutations.resolve_start_container
    reload_container = mutations.resolve_reload_container
    #stop_all_containers = mutations.resolve_stop_all_container
    #start_containers = mutations.resolve_start_containers
    
            
schema = strawberry.Schema( query=Query, mutation=Mutation )
graphql_app = GraphQL(schema)

app = FastAPI()

app.add_middleware(AuthorizationMiddleware)
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
    print("folder: " + folder)
    print(len(file))
    upload_dir = os.path.join(DATA_DIR, folder)
    await upload_file(file, upload_dir)
    if len(file): 
        return  {"success": 1, "file": {"url": f"https://210.102.178.108.nip.io/resource/file?folder={folder}&filename={file[0].filename}"}}
    return {"success": 1}

# @app.get('/auth')
# async def verify_user_container(request: Request, 
#                                 response: Response,
#                                 token: Optional[str] = None
#                                ):
#     auth_header = request.headers.get("Authorization")
#     uri = request.headers.get("x-original-uri")
#     cookie = request.headers.get("Cookie")
#     print(cookie)
#     token = uri.split('token=')[-1]

#     print(token)
#     #print(request.headers)
#     if auth_header == None : 
#         print("Unauthorized")
#         response.status_code = 200
#     else: response.status_code = 200
