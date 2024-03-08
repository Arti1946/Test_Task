import os
import re

import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def update_positions_top_100():
    """Обновление рейтинга репозиториев."""
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    with psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    ) as connection:
        with connection.cursor() as cursor:
            query = "SELECT * FROM repos ORDER BY stars DESC LIMIT 100"
            cursor.execute(query)
            result = cursor.fetchall()
            for i in range(len(result)):
                repo = result[i]
                repo_name = repo[1]
                position_cur = repo[3]
                if position_cur != i + 1:
                    q_for_upd = "UPDATE repos SET position_prev = %s, position_cur = %s WHERE repo = %s"
                    values = (position_cur, i + 1, repo_name)
                    cursor.execute(query=q_for_upd, vars=values)


def parse_github():
    """Парсинг данных из GitHub в базу данных."""
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    with psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    ) as connection:
        with connection.cursor() as cursor:
            github_url = (
                "https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&per_page=10"
                "&page=1"
            )
            r = requests.get(github_url).json()
            items = r.get("items")
            for item in items:
                full_name = item.get("full_name")
                owner = full_name.split("/")[0]
                stars = item.get("stargazers_count")
                watchers = item.get("watchers_count")
                forks = item.get("forks_count")
                open_issues = item.get("open_issues_count")
                language = item.get("language")
                if language is None:
                    language = "no-language"
                commits_url_raw = item.get("commits_url")
                commits_url = re.sub("{/...}", "", commits_url_raw)
                commits_url += "?per_page=59&page=1"
                commits = requests.get(commits_url).json()
                for commit in commits:
                    sha = commit.get("sha")
                    com = commit.get("commit")
                    commit_info = com.get("author")
                    author = commit_info.get("name")
                    date = commit_info.get("date")
                    cursor.execute(
                        """
                                       INSERT INTO commits (author, date, repo, repo_owner, sha) 
                                       VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                        (author, date, full_name, owner, sha),
                    )
                cursor.execute(
                    """
                    INSERT INTO repos (repo, owner, stars, watchers, forks, open_issues, language) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (repo) DO UPDATE SET (stars, watchers, forks, open_issues) = (
                        EXCLUDED.stars, EXCLUDED.watchers, EXCLUDED.forks, EXCLUDED.open_issues)""",
                    (
                        full_name,
                        owner,
                        stars,
                        watchers,
                        forks,
                        open_issues,
                        language,
                    ),
                )


def main(event, context):
    parse_github()
    update_positions_top_100()
