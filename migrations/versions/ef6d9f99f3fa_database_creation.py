"""Database creation

Revision ID: ef6d9f99f3fa
Revises: 
Create Date: 2024-03-06 02:15:53.004660

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ef6d9f99f3fa"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "repos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("repo", sa.String(), nullable=False),
        sa.Column("owner", sa.String(), nullable=False),
        sa.Column("position_cur", sa.Integer(), nullable=False),
        sa.Column("position_prev", sa.Integer(), nullable=False),
        sa.Column("stars", sa.Integer(), nullable=False),
        sa.Column("watchers", sa.Integer(), nullable=False),
        sa.Column("forks", sa.Integer(), nullable=False),
        sa.Column("open_issues", sa.Integer(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("repos")
    # ### end Alembic commands ###
