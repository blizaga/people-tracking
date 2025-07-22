from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.counter import Counter
from app.schemas.stats import StatsHistory, StatsLive

from datetime import datetime

router = APIRouter()

@router.get("/api/stats/", response_model=list[StatsHistory])
def get_stats_history(
    db: Session = Depends(get_db),
    start_date: datetime = None,
    end_date: datetime = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(Counter)
    if start_date:
        query = query.filter(Counter.updated_at >= start_date)
    if end_date:
        query = query.filter(Counter.updated_at <= end_date)

    results = query.offset(skip).limit(limit).all()
    return results


@router.get("/api/stats/live", response_model=list[StatsLive])
def get_stats_live(db: Session = Depends(get_db)):
    counters = db.query(Counter).all()
    return counters
