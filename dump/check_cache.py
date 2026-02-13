import sqlite3

conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

# Count cache entries
cursor.execute('SELECT COUNT(*) FROM resource_cache')
print(f'Total cache entries: {cursor.fetchone()[0]}')

# Show sample cache keys and their dates
cursor.execute('''
    SELECT cache_key, resource_title, provider, created_at 
    FROM resource_cache 
    LIMIT 20
''')

print('\nSample cached resources:')
for row in cursor.fetchall():
    print(f'  Key: {row[0][:32]}... | {row[1][:50]} | {row[2]} | {row[3]}')

conn.close()
