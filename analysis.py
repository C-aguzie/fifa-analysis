import pandas as pd
import unicodedata
import os

# Load data with proper encoding
df = pd.read_csv('fifa.csv', encoding='utf-8', low_memory=False)

# Clean column names
def clean_col(c):
    c = c.lower().replace(' ', '_')
    if 'ova' in c: return 'overall'
    if c == 'pot': return 'potential'
    if c == 'positions': return 'position'
    if c == 'w/f': return 'weak_foot'
    if c == 'sm': return 'skill_moves'
    if c == 'a/w': return 'attacking_work_rate'
    if c == 'd/w': return 'defensive_work_rate'
    if c == 'ir': return 'injury_resistance'
    return c

df.columns = [clean_col(c) for c in df.columns]

# Convert value/wage/release_clause
def conv(v):
    if pd.isna(v): return 0
    v = str(v).replace('€','').strip()
    if 'M' in v: return float(v.replace('M','')) * 1_000_000
    if 'K' in v: return float(v.replace('K','')) * 1_000
    try: return float(v)
    except: return 0

df['value'] = df['value'].apply(conv)
df['wage'] = df['wage'].apply(conv)
df['release_clause'] = df['release_clause'].apply(conv)

# Convert hits
def clean_hits(v):
    if pd.isna(v): return 0
    v = str(v).strip()
    if 'K' in v: return float(v.replace('K','')) * 1000
    try: return float(v)
    except: return 0

df['hits'] = df['hits'].apply(clean_hits)

# Fill missing
df = df.fillna({'club': 'Unknown', 'position': 'Unknown'})

# Clean all string columns - Normalize to ASCII (preserve as much as possible)
def clean_str(x):
    if pd.isna(x):
        return x
    s = str(x).replace('\n', ' ').replace('\r', ' ')
    # Normalize unicode to ASCII, ignore errors
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return ' '.join(s.split()).strip()

for col in df.columns:
    if df[col].dtype == 'object' or df[col].dtype == 'string':
        df[col] = df[col].apply(clean_str)

# Remove duplicates again after cleaning
df = df.drop_duplicates(subset=['name', 'team_&_contract'], keep='first')

# Save
os.makedirs('data', exist_ok=True)
df.to_csv('data/cleaned_fifa_final.csv', index=False)

# Display
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 200)
print('=== SAMPLE OF CLEANED DATA ===')
print(df[['name','longname','age','overall','potential','position','weak_foot','skill_moves']].head(20).to_string())
print(f'\n... Total rows: {len(df)}')
print('Data cleaned and saved successfully!')