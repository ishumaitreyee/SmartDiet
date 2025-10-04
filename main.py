from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import io

app = FastAPI()

# Allow all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
# --- All your backend data and functions ---
USERS = {}
FOOD_LOGS = {}

def next_id(store):
    return max(store.keys(), default=0) + 1

NUTRITION_TABLE = {
    "aloo_tikki": {"calories": 150, "protein": 3, "carbs": 25, "fat": 5},
    "butter_chicken": {"calories": 400, "protein": 30, "carbs": 10, "fat": 25},
    # ... (keep the rest of your nutrition table)
    "jaljeera": {"calories": 50, "protein": 1, "carbs": 12, "fat": 0.1},
}

# ... (keep all your other helper functions: get_nutrition, calc_bmr, etc.)
def get_nutrition(dish):
    dish_lower = dish.lower().replace(" ", "_")
    for key in NUTRITION_TABLE.keys():
        if key in dish_lower:
            return NUTRITION_TABLE[key]
    return {"calories": 200, "protein": 5, "carbs": 30, "fat": 5}

ACTIVITY_FACTORS = {
    'sedentary': 1.2,
    'light': 1.375,
    'moderate': 1.55,
    'active': 1.725,
}

def calc_bmr(age, weight, height, gender):
    if gender.lower().startswith('m'):
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def daily_calorie_needs(age, weight, height, gender, activity_level):
    bmr = calc_bmr(age, weight, height, gender)
    return int(bmr * ACTIVITY_FACTORS.get(activity_level, 1.2))

def recommend_daily_plan(calories, preference):
    if preference.startswith("veg"):
        return [("idli", 70), ("dal_makhani", 350), ("roti with sabzi", 300), ("fruit snack", 150)]
    else:
        return [("butter_chicken", 400), ("naan", 180), ("biryani", 450), ("gulab_jamun", 300)]

def preprocess_image_bytes(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img)
    arr = np.expand_dims(arr, axis=0).astype("float32")
    arr = preprocess_input(arr)
    return arr

def predict_dish_from_image(img_bytes):
    model = tf.keras.applications.MobileNetV2(weights="imagenet")
    arr = preprocess_image_bytes(img_bytes)
    preds = model.predict(arr)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0][0]
    
    dish = decoded[1]
    confidence = float(decoded[2])
    nutrition = get_nutrition(dish)
    return {
        "dish": dish,
        "confidence": confidence,
        "calories": nutrition["calories"],
        "protein": nutrition["protein"],
        "carbs": nutrition["carbs"],
        "fat": nutrition["fat"],
    }


# --- All your API endpoints MUST come BEFORE the final line ---
@app.post("/api/profile")
async def profile(
    age: int = Form(...), weight: float = Form(...), height: float = Form(...),
    gender: str = Form(...), activity_level: str = Form(...),
    preference: str = Form("veg"), name: str = Form(None)
):
    user_id = next_id(USERS)
    USERS[user_id] = {
        "id": user_id, "name": name, "age": age, "weight": weight, "height": height,
        "gender": gender, "activity_level": activity_level, "preference": preference,
    }
    return USERS[user_id]

@app.post("/api/recommend")
async def recommend(user_id: int = Form(...)):
    user = USERS.get(user_id)
    if not user:
        return {"error": "User not found"}
    calories = daily_calorie_needs(user["age"], user["weight"], user["height"],
                                  user["gender"], user["activity_level"])
    plan = recommend_daily_plan(calories, user["preference"])
    return {
        "calorie_needs": calories,
        "plan": [{"name": p[0], "calories": p[1]} for p in plan],
    }

@app.post("/api/upload_food")
async def upload_food(user_id: int = Form(...), file: UploadFile = File(...)):
    img_bytes = await file.read()
    result = predict_dish_from_image(img_bytes)
    if user_id not in FOOD_LOGS:
        FOOD_LOGS[user_id] = []
    FOOD_LOGS[user_id].append(result)
    return result

@app.get("/api/logs")
async def logs(user_id: int):
    return FOOD_LOGS.get(user_id, [])

# --- This MUST be the LAST line of code in the file ---
# It serves your frontend UI
app.mount("/", StaticFiles(directory="static", html=True), name="static")