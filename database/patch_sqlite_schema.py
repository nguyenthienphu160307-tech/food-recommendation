import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "food_recommendation.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# search_sessions
cur.execute("PRAGMA table_info(search_sessions)")
ss_cols = [c[1] for c in cur.fetchall()]
if "current_state" not in ss_cols:
    cur.execute("ALTER TABLE search_sessions ADD COLUMN current_state VARCHAR(50) DEFAULT 'SESSION_IDLE'")
    print("Added search_sessions.current_state")
if "ended_at" not in ss_cols:
    cur.execute("ALTER TABLE search_sessions ADD COLUMN ended_at DATETIME")
    print("Added search_sessions.ended_at")
if "closed_reason" not in ss_cols:
    cur.execute("ALTER TABLE search_sessions ADD COLUMN closed_reason VARCHAR(50)")
    print("Added search_sessions.closed_reason")

# notifications
cur.execute("PRAGMA table_info(notifications)")
notif_cols = [c[1] for c in cur.fetchall()]
if "content" not in notif_cols:
    cur.execute("ALTER TABLE notifications ADD COLUMN content TEXT")
    print("Added notifications.content")
if "type" not in notif_cols:
    cur.execute("ALTER TABLE notifications ADD COLUMN type VARCHAR(50) DEFAULT 'system'")
    print("Added notifications.type")

if "message" in notif_cols and "content" in notif_cols:
    cur.execute("UPDATE notifications SET content = message WHERE content IS NULL")
if "notification_type" in notif_cols and "type" in notif_cols:
    cur.execute("UPDATE notifications SET type = notification_type WHERE type IS NULL")

conn.commit()
print("Migration completed successfully.")
