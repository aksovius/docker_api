import os
from werkzeug.utils import secure_filename
import aiofiles
from fastapi.exceptions import HTTPException
import zipfile
from io import BytesIO
from fastapi.responses import  StreamingResponse
from config import ALLOWED_EXTENSIONS, CHUNK_SIZE

def allowed_file(filename, ALLOWED_EXTENSIONS):
    """Check if the file extension is allowed."""
    # Get the file extension
    extension = filename.rsplit('.', 1)[1].lower()
    # Check if the extension is allowed
    if extension in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
    
async def upload_file(file, upload_dir):
    # Check if directory exists, if not create it
    isExist = os.path.exists(upload_dir)
    if not isExist:
        os.makedirs(upload_dir) 
    # Loop through uploaded files and save them
    for f in file:
        # Check if file has a name
        if f.filename == '':
            next()
        # Check if file has correct file extension
        if f and allowed_file(f.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(f.filename)
           
            # Save file
            try:
                filepath = os.path.join(upload_dir, filename)
               
                async with aiofiles.open(filepath, 'wb') as data:
                    while chunk := await f.read(CHUNK_SIZE):
                        await data.write(chunk)
            except Exception:
                raise HTTPException(status_code=500, 
                    detail='There was an error uploading the file')
            finally:
                await f.close()
                print(filename, " saved")

async def upload_one_file(file, upload_dir):
    # Check if directory exists, if not create it
    isExist = os.path.exists(upload_dir)
    if not isExist:
        os.makedirs(upload_dir) 
    # Loop through uploaded files and save them
   
    # Check if file has a name
    if file.filename == '':
        next()
    # Check if file has correct file extension
    if file and allowed_file(file.filename, "jpg, jpeg, png"):
        filename = secure_filename(file.filename)
        # Save file
        try:
            filepath = os.path.join(upload_dir, filename)
            async with aiofiles.open(filepath, 'wb') as data:
                while chunk := await file.read(CHUNK_SIZE):
                    await data.write(chunk)
        except Exception:
            raise HTTPException(status_code=500, 
                detail='There was an error uploading the file')
        finally:
            await file.close()
            print(filename, " saved")

def zipfiles(file_list, study):
    io = BytesIO()
    zip_filename = "%s.zip" % study
    with zipfile.ZipFile(io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            zip.write(fpath, fpath.rsplit('/', 1)[1])
        #close zip
        zip.close()
    return StreamingResponse(
        iter([io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers = { "Content-Disposition":f"attachment;filename=%s" % zip_filename}
    )