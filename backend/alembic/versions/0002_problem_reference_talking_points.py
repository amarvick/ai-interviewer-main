"""add problem reference talking points"""

from alembic import op
import sqlalchemy as sa


revision = "0002_problem_reference_talking_points"
down_revision = "0001_eval_scale"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "problems",
        sa.Column("reference_talking_points", sa.JSON(), nullable=True),
    )
    op.execute(
        """
        UPDATE problems
        SET reference_talking_points = '[]'::json
        WHERE reference_talking_points IS NULL
        """
    )


def downgrade() -> None:
    op.drop_column("problems", "reference_talking_points")
