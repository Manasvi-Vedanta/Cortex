"""
Quick database check script
Verifies database has data in all tables
"""

import sqlite3

def check_database():
    """Check database contents."""
    print("="*60)
    print("  DATABASE CONTENTS CHECK")
    print("="*60)
    
    try:
        conn = sqlite3.connect('genmentor.db')
        cursor = conn.cursor()
        
        # Check all tables
        tables = {
            'occupations': 'Occupations (Career paths)',
            'skills': 'Skills',
            'occupation_skill_relations': 'Occupation-Skill Relations',
            'skill_skill_relations': 'Skill-Skill Relations',
            'votes': 'Community Votes',
            'suggestions': 'User Suggestions'
        }
        
        print("\n📊 Table Counts:")
        print("-" * 60)
        
        total_records = 0
        for table, description in tables.items():
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_records += count
                
                status = "✅" if count > 0 else "⚠️"
                print(f"{status} {description:.<40} {count:>10,}")
                
            except sqlite3.OperationalError as e:
                print(f"❌ {description:.<40} ERROR: {e}")
        
        print("-" * 60)
        print(f"   {'TOTAL RECORDS':.<40} {total_records:>10,}")
        
        # Show sample occupations
        print("\n🎓 Sample Occupations (first 5):")
        print("-" * 60)
        cursor.execute("SELECT preferred_label FROM occupations LIMIT 5")
        for i, (label,) in enumerate(cursor.fetchall(), 1):
            print(f"   {i}. {label}")
        
        # Show sample skills
        print("\n💡 Sample Skills (first 5):")
        print("-" * 60)
        cursor.execute("SELECT preferred_label FROM skills LIMIT 5")
        for i, (label,) in enumerate(cursor.fetchall(), 1):
            print(f"   {i}. {label}")
        
        # Check if votes exist
        print("\n👥 Community Engagement:")
        print("-" * 60)
        cursor.execute("SELECT COUNT(*) FROM votes")
        vote_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM suggestions")
        suggestion_count = cursor.fetchone()[0]
        
        if vote_count > 0:
            print(f"✅ Votes: {vote_count:,}")
            cursor.execute("""
                SELECT s.preferred_label, SUM(v.vote_value) as score
                FROM votes v
                JOIN skills s ON v.item_uri = s.concept_uri
                GROUP BY v.item_uri, s.preferred_label
                ORDER BY score DESC
                LIMIT 3
            """)
            print("   Top voted skills:")
            for label, score in cursor.fetchall():
                print(f"      • {label}: {score} votes")
        else:
            print(f"⚠️  No votes yet ({vote_count})")
        
        if suggestion_count > 0:
            print(f"✅ Suggestions: {suggestion_count:,}")
        else:
            print(f"⚠️  No suggestions yet ({suggestion_count})")
        
        conn.close()
        
        print("\n" + "="*60)
        if total_records > 10000:
            print("✅ Database is properly populated!")
        else:
            print("⚠️  Database may need setup (run setup_database.py)")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    check_database()
