"""
GenMentor Database Setup Script
This script creates and populates the SQLite database with ESCO data.
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path

def create_database_schema(cursor):
    """Create the database schema with all necessary tables."""
    
    # Create occupations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS occupations (
            concept_uri TEXT PRIMARY KEY,
            preferred_label TEXT NOT NULL,
            description TEXT,
            isco_group TEXT,
            alt_labels TEXT,
            scope_note TEXT,
            definition TEXT,
            status TEXT,
            modified_date TEXT
        )
    ''')
    
    # Create skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            concept_uri TEXT PRIMARY KEY,
            preferred_label TEXT NOT NULL,
            description TEXT,
            skill_type TEXT,
            reuse_level TEXT,
            alt_labels TEXT,
            scope_note TEXT,
            definition TEXT,
            status TEXT,
            modified_date TEXT,
            relevance_score REAL DEFAULT 1.0
        )
    ''')
    
    # Create occupation_skill_relations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS occupation_skill_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            occupation_uri TEXT NOT NULL,
            skill_uri TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            skill_type TEXT,
            FOREIGN KEY (occupation_uri) REFERENCES occupations (concept_uri),
            FOREIGN KEY (skill_uri) REFERENCES skills (concept_uri)
        )
    ''')
    
    # Create skill_skill_relations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_skill_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_skill_uri TEXT NOT NULL,
            target_skill_uri TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            source_skill_type TEXT,
            target_skill_type TEXT,
            FOREIGN KEY (source_skill_uri) REFERENCES skills (concept_uri),
            FOREIGN KEY (target_skill_uri) REFERENCES skills (concept_uri)
        )
    ''')
    
    # Create votes table for hybrid human feedback
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_uri TEXT NOT NULL,
            user_id TEXT NOT NULL,
            vote_value INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(item_uri, user_id)
        )
    ''')
    
    # Create suggestions table for hybrid human feedback
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_uri TEXT NOT NULL,
            user_id TEXT NOT NULL,
            suggestion_type TEXT NOT NULL,
            suggestion_text TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

def create_indexes(cursor):
    """Create indexes on URI columns for fast lookups."""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_occupations_uri ON occupations (concept_uri)",
        "CREATE INDEX IF NOT EXISTS idx_skills_uri ON skills (concept_uri)",
        "CREATE INDEX IF NOT EXISTS idx_occupation_skill_occupation ON occupation_skill_relations (occupation_uri)",
        "CREATE INDEX IF NOT EXISTS idx_occupation_skill_skill ON occupation_skill_relations (skill_uri)",
        "CREATE INDEX IF NOT EXISTS idx_skill_skill_source ON skill_skill_relations (source_skill_uri)",
        "CREATE INDEX IF NOT EXISTS idx_skill_skill_target ON skill_skill_relations (target_skill_uri)",
        "CREATE INDEX IF NOT EXISTS idx_votes_item ON votes (item_uri)",
        "CREATE INDEX IF NOT EXISTS idx_suggestions_item ON suggestions (item_uri)",
        "CREATE INDEX IF NOT EXISTS idx_occupations_label ON occupations (preferred_label)",
        "CREATE INDEX IF NOT EXISTS idx_skills_label ON skills (preferred_label)"
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)

def ingest_occupations_data(cursor, csv_path):
    """Ingest occupations data from CSV file."""
    print("Ingesting occupations data...")
    
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} occupations")
    
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO occupations 
            (concept_uri, preferred_label, description, isco_group, alt_labels, 
             scope_note, definition, status, modified_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row.get('conceptUri', ''),
            row.get('preferredLabel', ''),
            row.get('description', ''),
            row.get('iscoGroup', ''),
            row.get('altLabels', ''),
            row.get('scopeNote', ''),
            row.get('definition', ''),
            row.get('status', ''),
            row.get('modifiedDate', '')
        ))
    
    print("Occupations data ingested successfully!")

def ingest_skills_data(cursor, csv_path):
    """Ingest skills data from CSV file."""
    print("Ingesting skills data...")
    
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} skills")
    
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO skills 
            (concept_uri, preferred_label, description, skill_type, reuse_level,
             alt_labels, scope_note, definition, status, modified_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row.get('conceptUri', ''),
            row.get('preferredLabel', ''),
            row.get('description', ''),
            row.get('skillType', ''),
            row.get('reuseLevel', ''),
            row.get('altLabels', ''),
            row.get('scopeNote', ''),
            row.get('definition', ''),
            row.get('status', ''),
            row.get('modifiedDate', '')
        ))
    
    print("Skills data ingested successfully!")

def ingest_occupation_skill_relations(cursor, csv_path):
    """Ingest occupation-skill relations from CSV file."""
    print("Ingesting occupation-skill relations...")
    
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} occupation-skill relations")
    
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO occupation_skill_relations 
            (occupation_uri, skill_uri, relation_type, skill_type)
            VALUES (?, ?, ?, ?)
        ''', (
            row.get('occupationUri', ''),
            row.get('skillUri', ''),
            row.get('relationType', ''),
            row.get('skillType', '')
        ))
    
    print("Occupation-skill relations ingested successfully!")

def ingest_skill_skill_relations(cursor, csv_path):
    """Ingest skill-skill relations from CSV file."""
    print("Ingesting skill-skill relations...")
    
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} skill-skill relations")
    
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO skill_skill_relations 
            (source_skill_uri, target_skill_uri, relation_type, 
             source_skill_type, target_skill_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            row.get('originalSkillUri', ''),
            row.get('relatedSkillUri', ''),
            row.get('relationType', ''),
            row.get('originalSkillType', ''),
            row.get('relatedSkillType', '')
        ))
    
    print("Skill-skill relations ingested successfully!")

def main():
    """Main function to set up the database."""
    # Database file path
    db_path = 'genmentor.db'
    
    # CSV file paths
    csv_files = {
        'occupations': 'occupations_en.csv',
        'skills': 'skills_en.csv',
        'occupation_skill_relations': 'occupationSkillRelations_en.csv',
        'skill_skill_relations': 'skillSkillRelations_en.csv'
    }
    
    # Check if CSV files exist
    for file_type, file_path in csv_files.items():
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found!")
            return
    
    try:
        # Connect to SQLite database
        print("Connecting to database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create schema
        print("Creating database schema...")
        create_database_schema(cursor)
        
        # Create indexes
        print("Creating indexes...")
        create_indexes(cursor)
        
        # Ingest data
        ingest_occupations_data(cursor, csv_files['occupations'])
        ingest_skills_data(cursor, csv_files['skills'])
        ingest_occupation_skill_relations(cursor, csv_files['occupation_skill_relations'])
        ingest_skill_skill_relations(cursor, csv_files['skill_skill_relations'])
        
        # Commit changes
        conn.commit()
        print("\nDatabase setup completed successfully!")
        
        # Print some statistics
        cursor.execute("SELECT COUNT(*) FROM occupations")
        occ_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM skills")
        skill_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM occupation_skill_relations")
        occ_skill_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM skill_skill_relations")
        skill_skill_count = cursor.fetchone()[0]
        
        print(f"\nDatabase Statistics:")
        print(f"- Occupations: {occ_count:,}")
        print(f"- Skills: {skill_count:,}")
        print(f"- Occupation-Skill Relations: {occ_skill_count:,}")
        print(f"- Skill-Skill Relations: {skill_skill_count:,}")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
