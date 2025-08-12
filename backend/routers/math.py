from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.schemas import MathInput, MathResult, FactorialInput, FibonacciInput, HistoryItem
from models.orm import RequestLog
from typing import List
from services.cache import CacheService
import math
import asyncio
from auth.auth import get_current_user
import time

# ✅ Importuri corectate
from utils.kafka_utils import log_to_kafka
from utils.logger import log_json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pow", response_model=MathResult)
async def power(input: MathInput, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    cache = CacheService(db)
    cached = cache.get_cached_result("pow", input.dict())
    if cached is not None:
        log_to_kafka({
            "event": "pow",
            "input": input.dict(),
            "result": cached,
            "user": user,
            "cached": True,
            "time": time.time()
        })
        return {"result": cached}
    res = input.x ** input.y
    db.add(RequestLog(operation="pow", input_data=str(input.dict()), result=str(res)))
    db.commit()
    log_to_kafka({
        "event": "pow",
        "input": input.dict(),
        "result": res,
        "user": user,
        "cached": False,
        "time": time.time()
    })
    log_json(
        "pow calculated",
        event="pow",
        input=input.dict(),
        result=res,
        user=user,
        time=time.time()
    )
    return {"result": res}

@router.post("/factorial", response_model=MathResult)
async def factorial(input: FactorialInput, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    cache = CacheService(db)
    cached = cache.get_cached_result("factorial", input.dict())
    if cached is not None:
        log_to_kafka({
            "event": "factorial",
            "input": input.dict(),
            "result": cached,
            "user": user,
            "cached": True,
            "time": time.time()
        })
        return {"result": cached}
    n = input.x
    if n < 0:
        log_to_kafka({
            "event": "factorial",
            "input": input.dict(),
            "result": "Error: negative numbers not allowed",
            "user": user,
            "cached": False,
            "time": time.time()
        })
        return {"result": "Error: negative numbers not allowed"}
    res = math.factorial(n)
    db.add(RequestLog(operation="factorial", input_data=str(input.dict()), result=str(res)))
    db.commit()
    log_to_kafka({
        "event": "factorial",
        "input": input.dict(),
        "result": res,
        "user": user,
        "cached": False,
        "time": time.time()
    })
    log_json(
        "factorial calculated",
        event="factorial",
        input=input.dict(),
        result=res,
        user=user,
        time=time.time()
    )
    return {"result": res}

@router.post("/fibonacci", response_model=MathResult)
async def fibonacci(input: FibonacciInput, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    cache = CacheService(db)
    cached = cache.get_cached_result("fibonacci", input.dict())
    if cached is not None:
        log_to_kafka({
            "event": "fibonacci",
            "input": input.dict(),
            "result": cached,
            "user": user,
            "cached": True,
            "time": time.time()
        })
        return {"result": cached}
    n = input.x
    if n < 0:
        log_to_kafka({
            "event": "fibonacci",
            "input": input.dict(),
            "result": "Error: n must be non-negative",
            "user": user,
            "cached": False,
            "time": time.time()
        })
        return {"result": "Error: n must be non-negative"}
    if n in (0, 1):
        res = n
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        res = b
    db.add(RequestLog(operation="fibonacci", input_data=str(input.dict()), result=str(res)))
    db.commit()
    log_to_kafka({
        "event": "fibonacci",
        "input": input.dict(),
        "result": res,
        "user": user,
        "cached": False,
        "time": time.time()
    })
    log_json(
        "fibonacci calculated",
        event="fibonacci",
        input=input.dict(),
        result=res,
        user=user,
        time=time.time()
    )
    return {"result": res}

@router.get("/history", response_model=List[HistoryItem])
async def get_history(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    await asyncio.sleep(0)
    result = db.query(RequestLog).order_by(RequestLog.timestamp.desc()).all()
    log_to_kafka({
        "event": "history",
        "user": user,
        "action": "get_history",
        "time": time.time()
    })
    log_json(
        "history accessed",
        event="history",
        user=user,
        time=time.time()
    )
    return result

@router.delete("/history/{entry_id}")
async def delete_history(entry_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    entry = db.query(RequestLog).filter(RequestLog.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()
        log_to_kafka({
            "event": "history",
            "user": user,
            "action": "delete_entry",
            "entry_id": entry_id,
            "time": time.time()
        })
        log_json(
            "history entry deleted",
            event="history_delete",
            entry_id=entry_id,
            user=user,
            time=time.time()
        )
    return {"message": "Șters cu succes"}
