from fastapi import APIRouter, FastAPI, UploadFile, File, HTTPException
import uvicorn
from src.common.config.env_config import EnvConfig
from src.common.storage.minio_storage import MinioStorage

app = FastAPI()

# Inicializa o cliente MinIO
minio = MinioStorage(
    endpoint=EnvConfig.MINIO_ENDPOINT,
    access_key=EnvConfig.MINIO_ROOT_USER,
    secret_key=EnvConfig.MINIO_ROOT_PASSWORD,
    bucket_name=EnvConfig.MINIO_MAIN_BUCKET
)

print("✅ Connected! Buckets:", [b.name for b in minio.client.list_buckets()])

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        
        minio.upload(file)
        return {"message": "File uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/{filename}")
async def get_file(filename: str):
    try:
        file_data = minio.get_file_url(filename)
        return file_data  # pode retornar StreamingResponse se quiser baixar o arquivo
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

if __name__ == "__main__":
    print(f"Starting server on port {EnvConfig.APP_PORT}")
    uvicorn.run(app,
        host=EnvConfig.app_host(), 
        port=EnvConfig.APP_PORT,
        log_level="info"
    )
''''''