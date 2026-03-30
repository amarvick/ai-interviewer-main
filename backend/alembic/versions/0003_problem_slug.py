"""add slug column to problems"""

from alembic import op
import sqlalchemy as sa


revision = "0003_problem_slug"
down_revision = "0002_problem_reference_talking_points"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("problems", sa.Column("slug", sa.String(length=120), nullable=True))
    op.execute(
        """
        WITH generated AS (
            SELECT
                id,
                CASE
                    WHEN title IS NULL OR title = '' THEN id
                    ELSE regexp_replace(lower(title), '[^a-z0-9]+', '-', 'g')
                END AS base_slug
            FROM problems
        ),
        deduped AS (
            SELECT
                g.id,
                CASE WHEN g.base_slug = '' THEN g.id ELSE g.base_slug END AS cleaned_slug,
                ROW_NUMBER() OVER (PARTITION BY g.base_slug ORDER BY g.id) AS slug_rank
            FROM generated g
        )
        UPDATE problems AS p
        SET slug = CASE
            WHEN d.slug_rank = 1 THEN d.cleaned_slug
            ELSE d.cleaned_slug || '-' || d.slug_rank
        END
        FROM deduped d
        WHERE p.id = d.id AND (p.slug IS NULL OR p.slug = '')
        """
    )
    op.execute(
        """
        ALTER TABLE problems
            ALTER COLUMN slug SET NOT NULL
        """
    )
    op.create_unique_constraint("uq_problems_slug", "problems", ["slug"])


def downgrade() -> None:
    op.drop_constraint("uq_problems_slug", "problems", type_="unique")
    op.drop_column("problems", "slug")
