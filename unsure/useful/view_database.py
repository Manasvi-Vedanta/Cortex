"""
Quick Database Viewer for GenMentor
"""

import sqlite3
import sys

def view_database():
    """Interactive database viewer"""
    conn = sqlite3.connect('genmentor.db')
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("  GENMENTOR DATABASE VIEWER")
    print("="*70)
    
    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("\n📋 Available Tables:")
    for i, table in enumerate(tables, 1):
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"   {i}. {table[0]:<30} ({count:,} records)")
    
    print("\n" + "="*70)
    print("Quick Views:")
    print("="*70)
    
    # Show sample occupations
    print("\n🎓 Sample Occupations:")
    cursor.execute("SELECT preferred_label FROM occupations LIMIT 10")
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"   {i}. {row[0]}")
    
    # Show sample skills
    print("\n💡 Sample Skills:")
    cursor.execute("SELECT preferred_label FROM skills LIMIT 10")
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"   {i}. {row[0]}")
    
    # Show recent votes
    print("\n👍 Recent Community Votes:")
    cursor.execute("""
        SELECT s.preferred_label, v.vote_value, v.created_at 
        FROM votes v
        JOIN skills s ON v.item_uri = s.concept_uri
        ORDER BY v.created_at DESC
        LIMIT 5
    """)
    for row in cursor.fetchall():
        vote_emoji = "👍" if row[1] > 0 else "👎"
        print(f"   {vote_emoji} {row[0]} - {row[2]}")
    
    print("\n" + "="*70)
    conn.close()

if __name__ == "__main__":
    view_database()
