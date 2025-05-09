from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import pickle
import numpy as np

app = FastAPI()

# Load model and encoders
model = pickle.load(open('model.pkl', 'rb'))
encoders = pickle.load(open('encoders.pkl', 'rb'))

@app.get("/", response_class=HTMLResponse)
async def form():
    # Get unique values for dropdowns (from encoders)
    warehouse_options = encoders['Warehouse_block'].classes_
    shipment_options = encoders['Mode_of_Shipment'].classes_
    importance_options = encoders['Product_importance'].classes_
    gender_options = encoders['Gender'].classes_

    return f"""
    <h2>Shipment On-Time Prediction</h2>
    <form action="/predict_form" method="post">
        Warehouse Block: 
        <select name="Warehouse_block">
            {"".join([f'<option value="{x}">{x}</option>' for x in warehouse_options])}
        </select><br>

        Mode of Shipment: 
        <select name="Mode_of_Shipment">
            {"".join([f'<option value="{x}">{x}</option>' for x in shipment_options])}
        </select><br>

        Customer Care Calls: <input name="Customer_care_calls" type="number" /><br>
        Customer Rating: <input name="Customer_rating" type="number" /><br>
        Cost of Product: <input name="Cost_of_the_Product" type="number" /><br>
        Prior Purchases: <input name="Prior_purchases" type="number" /><br>

        Product Importance: 
        <select name="Product_importance">
            {"".join([f'<option value="{x}">{x}</option>' for x in importance_options])}
        </select><br>

        Gender: 
        <select name="Gender">
            {"".join([f'<option value="{x}">{x}</option>' for x in gender_options])}
        </select><br>

        Discount Offered: <input name="Discount_offered" type="number" /><br>
        Weight in gms: <input name="Weight_in_gms" type="number" /><br>

        <input type="submit" value="Predict" />
    </form>
    """

@app.post("/predict_form", response_class=HTMLResponse)
async def predict_form(
    Warehouse_block: str = Form(...),
    Mode_of_Shipment: str = Form(...),
    Customer_care_calls: int = Form(...),
    Customer_rating: int = Form(...),
    Cost_of_the_Product: int = Form(...),
    Prior_purchases: int = Form(...),
    Product_importance: str = Form(...),
    Gender: str = Form(...),
    Discount_offered: int = Form(...),
    Weight_in_gms: int = Form(...)
):
    try:
        # Encode categorical fields using label encoders
        block = encoders['Warehouse_block'].transform([Warehouse_block])[0]
        shipment = encoders['Mode_of_Shipment'].transform([Mode_of_Shipment])[0]
        importance = encoders['Product_importance'].transform([Product_importance])[0]
        gender = encoders['Gender'].transform([Gender])[0]

        # Build feature array
        features = np.array([[
            block, shipment, Customer_care_calls, Customer_rating,
            Cost_of_the_Product, Prior_purchases, importance, gender,
            Discount_offered, Weight_in_gms
        ]])

        # Get prediction
        prediction = model.predict(features)[0]
        message = "✅ Will arrive on time" if prediction == 1 else "❌ Will NOT arrive on time"
        return f"<h3>Prediction Result: {message}</h3>"

    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"
