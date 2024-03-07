from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime

metadata = MetaData()


repos = Table(
    "repos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("repo", String, nullable=False, unique=True),
    Column("owner", String, nullable=False),
    Column("position_cur", Integer),
    Column("position_prev", Integer),
    Column("stars", Integer, nullable=False),
    Column("watchers", Integer, nullable=False),
    Column("forks", Integer, nullable=False),
    Column("open_issues", Integer, nullable=False),
    Column("language", String, nullable=False),
)


commits = Table(
    "commits",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", DateTime, nullable=False),
    Column("author", String, nullable=False),
    Column("repo", String, nullable=False),
    Column("repo_owner", String, nullable=False),
    Column("sha", String, nullable=False, unique=True),
)
