from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# Encode username and password safely
username = quote_plus("Ahnaf")
password = quote_plus("Ahnaf@123")

# Correct URI
uri = f"mongodb+srv://{username}:{password}@cluster01.jigocqr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01"

# Create client
client = MongoClient(uri, server_api=ServerApi('1'))

# Test connection
try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)


# ---------------- FastAPI App ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow from anywhere (frontend)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Simple In-memory Token ----------------
TOKENS = {}

# ---------------- Login Route ----------------
@app.post("/login")
async def login(req: Request):
    data = await req.json()
    email = data.get("email")
    password = data.get("password")

    if email == "ahnaf@algorider.com" and password == "Algorider1233":
        token = str(uuid.uuid4())
        TOKENS[token] = email
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

# ---------------- Auth Helper ----------------
def check_token(token: str):
    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return TOKENS[token]

# ---------------- Add Problem ----------------
@app.post("/add_problem")
async def add_problem(req: Request):
    data = await req.json()
    token = data.get("token")
    user = check_token(token)

    problem = {
        "user": user,
        "title": data.get("title"),
        "rating": data.get("rating"),
        "date": data.get("date"),
        "feeling": data.get("feeling"),
        "notes": data.get("notes")
    }
    problems.insert_one(problem)
    return {"message": "Problem added successfully"}

# ---------------- Get All Problems ----------------
@app.get("/problems")
async def get_problems(token: str):
    user = check_token(token)
    user_problems = list(problems.find({"user": user}, {"_id": 0}))
    return {"problems": user_problems}

# ---------------- Root ----------------
@app.get("/")
def root():
    return {"message": "Simple Codeforces Practice API Running 🚀"}
