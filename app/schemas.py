from pydantic import BaseModel, Field
from typing import List, Optional

class AssessmentInput(BaseModel):
    age: int = Field(ge=13, le=100, default=22)
    height_cm: float = Field(gt=80, le=250, default=170)
    weight_kg: float = Field(gt=20, le=350, default=68)
    athlete: bool = False
    fruit_servings_day: float = Field(ge=0, le=15, default=2)
    vegetable_servings_day: float = Field(ge=0, le=20, default=3)
    protein_g_day: float = Field(ge=0, le=400, default=70)
    fibre_g_day: float = Field(ge=0, le=100, default=25)
    sugar_g_day: float = Field(ge=0, le=500, default=35)
    sodium_mg_day: float = Field(ge=0, le=15000, default=2000)
    fat_g_day: float = Field(ge=0, le=400, default=65)
    fried_meals_week: float = Field(ge=0, le=21, default=2)
    processed_meals_week: float = Field(ge=0, le=21, default=1)
    exercise_min_week: float = Field(ge=0, le=3000, default=150)
    sleep_hours_day: float = Field(ge=0, le=24, default=7.5)
    water_l_day: float = Field(ge=0, le=15, default=2.2)
    sedentary_hours_day: float = Field(ge=0, le=24, default=7)

class AssessmentResult(BaseModel):
    score: float
    risk_category: str
    recommendations: List[str]
    bmi: Optional[float] = None
    model_note: str
    assessment_id: Optional[int] = None
