"""Add username field to users

Revision ID: 248e28c2a024
Revises: dd80b8ef47ed
Create Date: 2024-12-11 11:46:06.415156

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "248e28c2a024"
down_revision: Union[str, None] = "dd80b8ef47ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("username", sa.String(), nullable=False))
    op.create_unique_constraint(None, "users", ["username"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.drop_column("users", "username")
    # ### end Alembic commands ###