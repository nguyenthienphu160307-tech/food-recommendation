"""Database migration script for Task TE9C654.

Creates the 6 interaction, search, and notification tables with full Foreign Keys and UNIQUE constraints:
- search_sessions (SearchSessions)
- search_messages (SearchMessages)
- search_criteria (SearchCriteria)
- restaurant_reviews (RestaurantReviews)
- user_favorites (UserFavorites)
- notifications (Notifications)
"""

from sqlalchemy import inspect
from app.core.database import engine, Base
import app.models  # noqa: F401 - Nạp toàn bộ model vào Base.metadata


def run_migration() -> list[str]:
    """Execute table creation and return list of created table names."""
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("=== MIGRATION TE9C654 COMPLETED SUCCESSFULLY ===")
    print(f"Total tables in database ({len(tables)}): {', '.join(sorted(tables))}")
    return tables


if __name__ == "__main__":
    run_migration()