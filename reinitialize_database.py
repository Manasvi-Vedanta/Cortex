"""
Database Cleanup and Reinitialization for Enhanced Features
This script drops old feedback tables and recreates them with proper schema.
"""

import sqlite3
import os

DB_PATH = 'genmentor.db'

print("=" * 80)
print("DATABASE CLEANUP AND REINITIALIZATION")
print("=" * 80)

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# List of feedback tables to clean
feedback_tables = [
    'votes',
    'suggestions',
    'suggestion_votes',
    'curriculum_updates',
    'resource_ratings',
    'learning_resources',
    'resource_tags',
    'resource_access_stats'
]

print("\nStep 1: Checking existing tables...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
existing_tables = [row[0] for row in cursor.fetchall()]
print(f"Found {len(existing_tables)} total tables in database")

print("\nStep 2: Dropping old feedback tables (if they exist)...")
for table in feedback_tables:
    if table in existing_tables:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"  ✓ Dropped table: {table}")
        except Exception as e:
            print(f"  ✗ Error dropping {table}: {e}")
    else:
        print(f"  - Table {table} doesn't exist (skipping)")

conn.commit()
print("✓ Old tables dropped successfully")

print("\nStep 3: Reinitializing Community Feedback System...")
try:
    from community_feedback import CommunityFeedbackSystem
    feedback = CommunityFeedbackSystem()
    print("✓ Community Feedback System initialized")
    print("  Created tables: votes, suggestions, suggestion_votes, curriculum_updates, resource_ratings")
except Exception as e:
    print(f"✗ Error: {e}")

print("\nStep 4: Reinitializing Resource Curator...")
try:
    from resource_curator import ResourceCurator
    curator = ResourceCurator()
    print("✓ Resource Curator initialized")
    print("  Created tables: learning_resources, resource_tags, resource_access_stats")
except Exception as e:
    print(f"✗ Error: {e}")

print("\nStep 5: Verifying new tables...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ({})".format(
    ','.join(['?' for _ in feedback_tables])
), feedback_tables)
new_tables = [row[0] for row in cursor.fetchall()]
print(f"✓ Successfully created {len(new_tables)} feedback tables:")
for table in new_tables:
    # Get column info
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    print(f"\n  Table: {table}")
    print(f"  Columns: {', '.join([col[1] for col in columns])}")

conn.close()

print("\n" + "=" * 80)
print("✓ DATABASE REINITIALIZATION COMPLETE")
print("=" * 80)
print("\nYou can now run: python test_enhanced_features.py")
