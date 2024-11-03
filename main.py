from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

from typing import List, Dict, Any, Optional

app = FastAPI()

# MongoDB connection string
MONGODB_URI = "mongodb://localhost:27017/"
client = AsyncIOMotorClient(MONGODB_URI)
db = client.mydatabase  # Replace 'mydatabase' with your actual database name

# Pydantic models for the data structure
class Direction(BaseModel):
    name: str

class Laboratory(BaseModel):
    name: str

# Helper function to convert MongoDB document to JSON-serializable format
def serialize_document(document):
    document["_id"] = str(document["_id"])  # Convert ObjectId to string
    return document

# Route to create a new direction
@app.post("/directions/", response_model=Direction)
async def create_direction(direction: Direction):
    direction_dict = direction.dict()
    result = await db.direction.insert_one(direction_dict)
    return {"name": direction_dict["name"]}

# Route to get all directions
@app.get("/directions/")
async def read_directions():
    directions = []
    async for direction in db.direction.find():
        directions.append(serialize_document(direction))
    return directions

# Route to create a new laboratory
@app.post("/laboratories/", response_model=Laboratory)
async def create_laboratory(laboratory: Laboratory):
    laboratory_dict = laboratory.dict()
    result = await db.laboratory.insert_one(laboratory_dict)
    return {"name": laboratory_dict["name"]}

# Route to get all laboratories
@app.get("/laboratories/")
async def read_laboratories():
    laboratories = []
    async for laboratory in db.laboratory.find():
        laboratories.append(serialize_document(laboratory))
    return laboratories

















# Define the application model (excluding files)
class ApplicationModel(BaseModel):
    name: str
    company: str
    description: str
    directionID: int
    budget: int
    contact: str
    notes: Optional[str] = None
    fio: str

# Route to create a new application
@app.post("/applications/")
async def create_application(
    name: str = Form(...),
    company: str = Form(...),
    description: str = Form(...),
    directionID: int = Form(...),
    budget: int = Form(...),
    contact: str = Form(...),
    notes: Optional[str] = Form(None),
    fio: str = Form(...),
    projectFile: List[UploadFile] = File(...)
):
    # Prepare the application data
    application_data = {
        "name": name,
        "company": company,
        "description": description,
        "directionID": directionID,
        "budget": budget,
        "contact": contact,
        "notes": notes,
        "fio": fio,
        "projectFile": []  # To store file information
    }
    
    # Process and save the uploaded files (in memory for now)
    for file in projectFile:
        content = await file.read()  # Read file content
        application_data["projectFile"].append({
            "filename": file.filename,
            "content_type": file.content_type,
            "content": content  # Store file content in MongoDB, though it's generally better to store it elsewhere
        })

    # Insert application data into MongoDB
    result = await db.applications.insert_one(application_data)
    return {"id": str(result.inserted_id)}


@app.get("/applications/", response_model=List[Dict[str, Any]])
async def get_applications():
    applications = []
    try:
        async for app in db["applications"].find():
            serialized_app = serialize_document(app)
            applications.append(serialized_app)
        return applications
    except Exception as e:
        return {"error": str(e)}  # Return error details


















# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
