from fastapi import FastAPI, HTTPException, Depends
from supabase import create_client, Client
from pydantic import BaseModel
import os


app = FastAPI(title="Bytebase User Management API")

url: str = "https://gotqstxlcbtuafmffcia.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdvdHFzdHhsY2J0dWFmbWZmY2lhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg5MTY1NywiZXhwIjoyMDc5NDY3NjU3fQ.WZ8nGY0plK283eHywNihleK5Id1D1EazNqGJbbpI40U" # 别泄露给前端，仅在后端使用
supabase: Client = create_client(url, key)

class DeleteRequest(BaseModel):
    user_id: str

@app.get("/")
def read_root():
    return {"message": "Bytebase User Management API is running"}

@app.get("/users")
def get_all_users():
    """
    获取用户列表接口
    """
    try:
        response = supabase.auth.admin.list_users()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/delete")
def delete_user(request: DeleteRequest):
    try:
        response = supabase.auth.admin.delete_user(request.user_id)
        return {"message": f"User {request.user_id} deleted successfully", "details": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)