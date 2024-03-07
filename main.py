from datetime import datetime

from databases import Database
from fastapi import FastAPI

from core.config import DB_URL

app = FastAPI()
db = Database(DB_URL, min_size=5, max_size=20)


@app.on_event("startup")
async def startup():
    """Подключение к базе данных при запуске приложения."""
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    """Закрытие соединения с базой данных при отключении приложения."""
    await db.disconnect()


@app.get("/api/repos/top100/")
async def get_top100():
    query = "SELECT * FROM repos ORDER BY stars DESC LIMIT 100"
    result = await db.fetch_all(query)
    return result


@app.get("/api/repos/{owner}/{repo}/activity/")
async def get_repo_activity(
    owner: str, repo: str, until: datetime, since: datetime
):
    repo_full_name = f"{owner}/{repo}"
    query = (
        (
            """
             SELECT DISTINCT date_trunc('day', date) AS date,
                 STRING_TO_ARRAY(STRING_AGG(DISTINCT author, ', '), ', ', '') AS authors,
             COUNT(*) AS commits 
             FROM commits 
             WHERE repo = :repo and repo_owner = :owner AND date BETWEEN :since AND :until 
             GROUP BY date_trunc('day', date)
             """
        ),
    )
    values = {
        "repo": repo_full_name,
        "owner": owner,
        "since": since,
        "until": until,
    }
    result = await db.fetch_all(query=query, values=values)
    return result
