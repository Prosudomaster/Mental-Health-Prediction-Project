from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

model = joblib.load("Mental_Health_Model.pkl")

app = FastAPI()

# CORS (Cross Origin Resource Sharing) to share data between front-end and back-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# A First Pydantic Model for Data Type Validation
class StudentData(BaseModel):
    age: int = Field(..., ge=10, le=100)
    gender: Literal["Male", "Female"]
    country: str
    academic_level: Literal["Undergraduate", "Graduate", "High School"]
    most_used_platform: Literal[
        "Facebook",
        "LinkedIn",
        "Instagram",
        "Snapchat",
        "Twitter",
        "YouTube",
        "TikTok",
        "LINE",
        "KakaoTalk",
        "VKontakte",
        "WhatsApp",
        "WeChat",
    ]
    purpose_of_use: Literal["Networking", "Education", "Entertainment", "News"]
    avg_daily_usage_hours: float = Field(..., ge=0, le=14)
    daily_unlocks: int = Field(
        ..., ge=0
    )  # if Field Important/Necessary use "..." three dots
    study_hours: float = Field(
        ..., ge=0, le=24
    )  # Field used in number values (float, int) and Literal used in str values
    physical_activity_hours: float = Field(..., ge=0, le=24)
    sleep_hours_per_night: float = Field(..., ge=0, le=24)
    stress_level: Literal["Medium", "Low", "Very High", "High"]


# Describe What we send back
class PredictionResponse(BaseModel):
    predicted_mental_health_score: float


@app.get("/")
def great():
    return {"Welcome to Sheryians AI School"}


top_countries = [
    "Other",
    "India",
    "USA",
    "Canada",
    "Australia",
    "UK",
    "Germany",
    "Mexico",
    "Turkey",
    "France",
]


@app.post("/predict", response_model=PredictionResponse)
def predict(data: StudentData):

    country_group = data.country if data.country in top_countries else "other"

    input_row = pd.DataFrame(
        [
            {
                "Age": data.age,
                "Gender": data.gender,
                "Country": data.country,
                "Academic_Level": data.academic_level,
                "Most_Used_Platform": data.most_used_platform,
                "Purpose_Of_Use": data.purpose_of_use,
                "Avg_Daily_Usage_Hours": data.avg_daily_usage_hours,
                "Daily_Unlocks": data.daily_unlocks,
                "Study_Hours": data.study_hours,
                "Physical_Activity_Hours": data.physical_activity_hours,
                "Sleep_Hours_Per_Night": data.sleep_hours_per_night,
                "Stress_Level": data.stress_level,
                "Grouped_country": country_group,
            }
        ]
    )

    prediction = model.predict(input_row)[0]
    return PredictionResponse(predicted_mental_health_score=round(float(prediction), 2))
