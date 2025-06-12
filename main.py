from fastapi import FastAPI, HTTPException
from database import expenses_collection
from models import Expense
from utils import calculate_balances, simplify_settlements
from bson import ObjectId

app = FastAPI()

# Expense Management
@app.post("/expenses")
def add_expense(exp: Expense):
    if not exp.description or not exp.paid_by:
        raise HTTPException(status_code=400, detail="Missing required fields.")
    result = expenses_collection.insert_one(exp.dict())
    return {"success": True, "message": "Expense added successfully", "id": str(result.inserted_id)}

@app.get("/expenses")
def get_expenses():
    return list(expenses_collection.find({}, {"_id": 0}))

@app.put("/expenses/{id}")
def update_expense(id: str, exp: Expense):
    result = expenses_collection.update_one({"_id": ObjectId(id)}, {"$set": exp.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"success": True, "message": "Expense updated"}

@app.delete("/expenses/{id}")
def delete_expense(id: str):
    result = expenses_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"success": True, "message": "Expense deleted"}

# Settlements & Balances
@app.get("/balances")
def get_balances():
    expenses = list(expenses_collection.find())
    balances = calculate_balances(expenses)
    return balances

@app.get("/settlements")
def get_settlements():
    expenses = list(expenses_collection.find())
    balances = calculate_balances(expenses)
    return simplify_settlements(balances)

@app.get("/people")
def get_people():
    people = set()
    for exp in expenses_collection.find():
        people.add(exp["paid_by"])
        if exp.get("shared_by"):
            people.update(exp["shared_by"])
    return sorted(list(people))
