"""Add language column to users

Revision ID: bada262bb9fe
Revises: ab30fb23bad8
Create Date: 2024-12-05 18:25:30.681592

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "bada262bb9fe"
down_revision: Union[str, None] = "ab30fb23bad8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    postgresql.ENUM("EN", "RU", name="languageenum").create(op.get_bind())
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("language", sa.Enum("EN", "RU", name="languageenum"), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "language")
    # ### end Alembic commands ###
    postgresql.ENUM("EN", "RU", name="languageenum").drop(op.get_bind())
