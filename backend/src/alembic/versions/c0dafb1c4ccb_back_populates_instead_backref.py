"""back_populates instead backref

Revision ID: c0dafb1c4ccb
Revises: 154b0551532f
Create Date: 2023-09-20 16:32:56.094340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c0dafb1c4ccb"
down_revision: Union[str, None] = "154b0551532f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
