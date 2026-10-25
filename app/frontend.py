import os, requests, pandas as pd, streamlit as st
from app.nutrition import FOODS
API_URL=os.getenv("API_URL","http://localhost:8000")
st.set_page_config(page_title="Lifestyle Monitor",page_icon="🌿",layout="wide")
st.title("🌿 AI-Based Personalized Health & Lifestyle Risk Monitoring")
st.caption("ML + MLOps demo • Not a medical diagnosis")
with st.sidebar:
    st.header("About this demo")
    st.write("Enter typical-day nutrition and lifestyle averages.")
    st.warning("Model training data and score labels are synthetic and not clinically validated.")
st.subheader("1. Food lookup")
food_name=st.selectbox("Choose a demo food item",list(FOODS.keys()))
servings=st.number_input("Number of servings",min_value=.25,max_value=10.0,value=1.0,step=.25)
food=FOODS[food_name]
cols=st.columns(4)
for col,label,key in zip(cols,["Calories","Protein (g)","Fibre (g)","Sodium (mg)"],["calories","protein_g","fibre_g","sodium_mg"]):
    col.metric(label,round(food[key]*servings,1))
st.caption("Approximate illustrative catalogue values per serving. Extend with verified data before research use.")
st.subheader("2. Lifestyle information")
with st.form("assessment"):
    a,b,c=st.columns(3)
    with a:
        age=st.number_input("Age",13,100,22); height=st.number_input("Height (cm)",100.0,250.0,170.0); weight=st.number_input("Weight (kg)",25.0,300.0,68.0)
        athlete=st.checkbox("Highly muscular / athletic"); fruit=st.number_input("Fruit servings/day",0.0,15.0,2.0,.5); veg=st.number_input("Vegetable servings/day",0.0,20.0,3.0,.5)
    with b:
        protein=st.number_input("Protein (g/day)",0.0,400.0,70.0); fibre=st.number_input("Fibre (g/day)",0.0,100.0,25.0); sugar=st.number_input("Sugar (g/day)",0.0,500.0,35.0)
        sodium=st.number_input("Sodium (mg/day)",0.0,15000.0,2000.0); fat=st.number_input("Fat (g/day)",0.0,400.0,65.0); fried=st.number_input("Fried meals/week",0.0,21.0,2.0)
    with c:
        processed=st.number_input("Processed meals/week",0.0,21.0,1.0); exercise=st.number_input("Exercise (minutes/week)",0.0,3000.0,150.0)
        sleep=st.number_input("Sleep (hours/day)",0.0,24.0,7.5,.5); water=st.number_input("Water (litres/day)",0.0,15.0,2.2,.1); sedentary=st.number_input("Sedentary time (hours/day)",0.0,24.0,7.0,.5)
    submitted=st.form_submit_button("Analyze lifestyle pattern",type="primary",use_container_width=True)
if submitted:
    payload={"age":int(age),"height_cm":height,"weight_kg":weight,"athlete":athlete,"fruit_servings_day":fruit,"vegetable_servings_day":veg,"protein_g_day":protein,"fibre_g_day":fibre,"sugar_g_day":sugar,"sodium_mg_day":sodium,"fat_g_day":fat,"fried_meals_week":fried,"processed_meals_week":processed,"exercise_min_week":exercise,"sleep_hours_day":sleep,"water_l_day":water,"sedentary_hours_day":sedentary}
    try:
        with st.spinner("Validating data and running model..."): r=requests.post(f"{API_URL}/predict",json=payload,timeout=30)
        if r.ok:
            out=r.json(); st.success("Analysis completed")
            x,y,z=st.columns(3); x.metric("Lifestyle score (demo)",f"{out['score']:.1f}/100"); y.metric("Pattern category (demo)",out["risk_category"]); z.metric("BMI (context only)",out["bmi"])
            st.progress(min(1,max(0,out["score"]/100))); st.subheader("Pattern-based suggestions")
            for rec in out["recommendations"]: st.write("• "+rec)
            st.info(out["model_note"]); st.caption(f"Assessment ID: {out.get('assessment_id') or 'not saved'}")
        else: st.error(f"API error {r.status_code}: {r.text}")
    except requests.RequestException as e: st.error(f"Could not reach API at {API_URL}. Check Docker Compose. {e}")
st.divider(); st.subheader("3. Recent assessment history")
try:
    r=requests.get(f"{API_URL}/history",timeout=5)
    if r.ok and r.json(): st.dataframe(pd.DataFrame(r.json()),use_container_width=True,hide_index=True)
    else: st.caption("No saved assessments yet.")
except requests.RequestException: st.caption("History is unavailable until API is running.")
st.divider(); st.caption("Educational prototype only. Not for diagnosis, treatment, or medical decisions.")
