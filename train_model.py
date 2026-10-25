# Train educational models on synthetic rows. These are not clinical labels.
import os, json
from pathlib import Path
import numpy as np, pandas as pd, joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, precision_recall_fscore_support

SEED=42
OUT=Path(os.getenv("MODEL_PATH","models/models.joblib")); OUT.parent.mkdir(parents=True,exist_ok=True)
FEATURES=["age","height_cm","weight_kg","athlete","fruit_servings_day","vegetable_servings_day","protein_g_day","fibre_g_day","sugar_g_day","sodium_mg_day","fat_g_day","fried_meals_week","processed_meals_week","exercise_min_week","sleep_hours_day","water_l_day","sedentary_hours_day"]
def make_data(n=6000):
    r=np.random.default_rng(SEED)
    d=pd.DataFrame({
      "age":r.integers(18,75,n),"height_cm":r.normal(170,10,n).clip(140,205),"weight_kg":r.normal(72,16,n).clip(40,150),"athlete":r.integers(0,2,n),
      "fruit_servings_day":r.gamma(1.8,1,n).clip(0,8),"vegetable_servings_day":r.gamma(2,1,n).clip(0,10),
      "protein_g_day":r.normal(75,28,n).clip(10,200),"fibre_g_day":r.normal(23,9,n).clip(0,60),"sugar_g_day":r.gamma(2.2,18,n).clip(0,180),
      "sodium_mg_day":r.normal(2400,900,n).clip(300,7000),"fat_g_day":r.normal(70,25,n).clip(15,180),
      "fried_meals_week":r.poisson(2.4,n).clip(0,14),"processed_meals_week":r.poisson(2,n).clip(0,14),
      "exercise_min_week":r.gamma(2,65,n).clip(0,700),"sleep_hours_day":r.normal(7.1,1.3,n).clip(3,12),
      "water_l_day":r.normal(2,.7,n).clip(.3,5),"sedentary_hours_day":r.normal(8,2.5,n).clip(1,16)})
    score=(50+2.2*d.fruit_servings_day.clip(0,5)+2*d.vegetable_servings_day.clip(0,6)+.22*d.fibre_g_day.clip(0,40)+.035*d.protein_g_day.clip(0,120)+.025*d.exercise_min_week.clip(0,300)-.12*d.sugar_g_day.clip(0,100)-.003*d.sodium_mg_day.clip(0,4000)-1.8*d.fried_meals_week-1.5*d.processed_meals_week-.06*d.fat_g_day.clip(0,120)-.7*d.sedentary_hours_day+1.8*(7.5-(d.sleep_hours_day-7.5).abs()).clip(-2,1))
    d["target_score"]=np.clip(score+r.normal(0,3.5,n),0,100)
    d["target_risk"]=np.select([d.target_score>=75,d.target_score>=55],[0,1],default=2)
    return d
def main():
    d=make_data(); X=d[FEATURES].astype(float); y=d.target_score
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=SEED)
    reg=RandomForestRegressor(n_estimators=150,max_depth=12,min_samples_leaf=3,random_state=SEED,n_jobs=-1).fit(Xtr,ytr)
    p=reg.predict(Xte); mae=float(mean_absolute_error(yte,p)); rmse=float(np.sqrt(mean_squared_error(yte,p))); r2=float(r2_score(yte,p))
    Xtr,Xte,ytr,yte=train_test_split(X,d.target_risk,test_size=.2,random_state=SEED,stratify=d.target_risk)
    clf=RandomForestClassifier(n_estimators=150,max_depth=12,min_samples_leaf=3,random_state=SEED,class_weight="balanced",n_jobs=-1).fit(Xtr,ytr)
    pc=clf.predict(Xte); acc=float(accuracy_score(yte,pc)); pr,re,f1,_=precision_recall_fscore_support(yte,pc,average="weighted",zero_division=0)
    joblib.dump({"regressor":reg,"classifier":clf,"features":FEATURES},OUT)
    metrics={"MAE":mae,"RMSE":rmse,"R2":r2,"classification_accuracy":acc,"weighted_precision":float(pr),"weighted_recall":float(re),"weighted_f1":float(f1)}
    print("Saved",OUT.resolve()); print(json.dumps(metrics,indent=2))
    uri=os.getenv("MLFLOW_TRACKING_URI")
    if uri:
      try:
        import mlflow
        mlflow.set_tracking_uri(uri); mlflow.set_experiment("health-lifestyle-demo")
        with mlflow.start_run(run_name="random-forest-synthetic-demo"):
          mlflow.log_params({"seed":SEED,"n_samples":len(d),"n_estimators":150,"max_depth":12})
          mlflow.log_metrics(metrics); mlflow.log_artifact(str(OUT),artifact_path="model_bundle")
          mlflow.set_tag("data_type","synthetic_demo"); mlflow.set_tag("clinical_validation","false")
        print("Logged experiment to MLflow")
      except Exception as e: print("MLflow logging skipped:",e)
if __name__=="__main__": main()
