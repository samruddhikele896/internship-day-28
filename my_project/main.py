from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Daily Expense Tracker API")

# ====================================================
# Initial Balance APIs
# ====================================================

@app.post("/balance", response_model=schemas.InitialBalanceResponse)
def create_balance(balance: schemas.InitialBalanceCreate,
                   db: Session = Depends(get_db)):

    new_balance = models.InitialBalance(
        total_amount=balance.total_amount
    )

    db.add(new_balance)
    db.commit()
    db.refresh(new_balance)

    return new_balance


@app.get("/balance", response_model=schemas.InitialBalanceResponse)
def get_balance(db: Session = Depends(get_db)):
    balance = db.query(models.InitialBalance).order_by(
        models.InitialBalance.created_at.desc()
    ).first()

    if not balance:
        raise HTTPException(status_code=404, detail="Initial balance not found")

    return balance


@app.put("/balance/{balance_id}",
         response_model=schemas.InitialBalanceResponse)
def update_balance(balance_id: int,
                   balance: schemas.InitialBalanceCreate,
                   db: Session = Depends(get_db)):

    data = db.query(models.InitialBalance).filter(
        models.InitialBalance.id == balance_id
    ).first()

    if not data:
        raise HTTPException(status_code=404,
                            detail="Balance not found")

    data.total_amount = balance.total_amount

    db.commit()
    db.refresh(data)

    return data


# ====================================================
# Expense APIs
# ====================================================

@app.post("/expenses", response_model=schemas.ExpenseResponse)
def add_expense(expense: schemas.ExpenseCreate,
                db: Session = Depends(get_db)):

    new_expense = models.Expense(
        expense_for=expense.expense_for,
        amount=expense.amount
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@app.get("/expenses", response_model=list[schemas.ExpenseResponse])
def get_all_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()


@app.get("/expenses/{expense_id}",
         response_model=schemas.ExpenseResponse)
def get_expense(expense_id: int,
                db: Session = Depends(get_db)):

    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if not expense:
        raise HTTPException(status_code=404,
                            detail="Expense not found")

    return expense


@app.put("/expenses/{expense_id}",
         response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int,
                   data: schemas.ExpenseCreate,
                   db: Session = Depends(get_db)):

    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if not expense:
        raise HTTPException(status_code=404,
                            detail="Expense not found")

    expense.expense_for = data.expense_for
    expense.amount = data.amount

    db.commit()
    db.refresh(expense)

    return expense


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int,
                   db: Session = Depends(get_db)):

    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if not expense:
        raise HTTPException(status_code=404,
                            detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}


# ====================================================
# Saving Goal APIs
# ====================================================

@app.post("/goals", response_model=schemas.SavingGoalResponse)
def create_goal(goal: schemas.SavingGoalCreate,
                db: Session = Depends(get_db)):

    new_goal = models.SavingGoal(
        monthly_goal=goal.monthly_goal,
        weekly_goal=goal.weekly_goal,
        daily_goal=goal.daily_goal
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return new_goal


@app.get("/goals",
         response_model=list[schemas.SavingGoalResponse])
def get_goals(db: Session = Depends(get_db)):
    return db.query(models.SavingGoal).all()


@app.put("/goals/{goal_id}",
         response_model=schemas.SavingGoalResponse)
def update_goal(goal_id: int,
                goal: schemas.SavingGoalCreate,
                db: Session = Depends(get_db)):

    data = db.query(models.SavingGoal).filter(
        models.SavingGoal.id == goal_id
    ).first()

    if not data:
        raise HTTPException(status_code=404,
                            detail="Goal not found")

    data.monthly_goal = goal.monthly_goal
    data.weekly_goal = goal.weekly_goal
    data.daily_goal = goal.daily_goal

    db.commit()
    db.refresh(data)

    return data