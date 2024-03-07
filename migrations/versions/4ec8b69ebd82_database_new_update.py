"""Database new update

Revision ID: 4ec8b69ebd82
Revises: bdd7bfd60a43
Create Date: 2024-03-06 18:38:34.083010

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4ec8b69ebd82"
down_revision: Union[str, None] = "bdd7bfd60a43"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "commits", sa.Column("repo_owner", sa.String(), nullable=False)
    )
    op.drop_constraint("commits_repo_fkey", "commits", type_="foreignkey")
    op.alter_column(
        "commits",
        "repo",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        "commits_repo_fkey", "commits", "repos", ["repo"], ["id"]
    )
    op.alter_column(
        "commits",
        "repo",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_column("commits", "repo_owner")
    # ### end Alembic commands ###
