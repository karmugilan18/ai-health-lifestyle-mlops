# AI-Based Personalized Health & Lifestyle Risk Monitoring System
Demo-ready ML + MLOps project using FastAPI, Streamlit, scikit-learn, MLflow, PostgreSQL, Docker Compose, Prometheus and Grafana.

> Educational prototype only. Training data and score labels are synthetic; this is not a medical diagnostic system and is not clinically validated.

## Run
1. Extract this ZIP and open the `ai_health_lifestyle_mlops` folder in VS Code.
2. Install Docker Desktop and start it.
3. Open a terminal in this folder and run:
   ```bash
   docker compose up --build
   ```
4. Open:
   - Streamlit app: http://localhost:8501
   - FastAPI docs: http://localhost:8000/docs
   - MLflow: http://localhost:5000
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (login `admin` / `admin`)
5. Stop with `docker compose down`. To remove database history too: `docker compose down -v`.

## Demo walkthrough
Enter a typical-day set of nutrition/lifestyle values, click **Analyze lifestyle pattern**, and show the score, pattern category, recommendations and saved history. Then show FastAPI docs, MLflow runs and the Grafana dashboard.

## Data sources and limitations
For a reliable offline demo, the app includes a small illustrative food catalogue and generates synthetic training rows. It does not claim to have downloaded or merged real datasets. For research-grade data, consider:
- USDA FoodData Central (food composition): https://fdc.nal.usda.gov/
- NHANES (dietary, examination and questionnaire data): https://www.cdc.gov/nchs/nhanes/
- UCI PAMAP2 (wearable activity reference data): https://archive.ics.uci.edu/dataset/231/pamap2+physical+activity+monitoring

These sources do not contain all required fields in a common schema; integration needs mapping, preprocessing, licensing review and validation.

## ML design
- RandomForestRegressor predicts an illustrative 0–100 score.
- RandomForestClassifier predicts Low / Moderate / High demo category.
- MAE, RMSE, R², accuracy, precision, recall and F1 are printed and logged to MLflow.
- Recommendations use transparent rules tied to input patterns.
- Synthetic data performance does not prove real-world validity.

## Important viva point
The novelty is the integration of multi-factor lifestyle features, factor-based recommendations, historical tracking and a reproducible MLOps deployment—not the invention of food tracking.
