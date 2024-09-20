import pandas as pd

def normalise_author_ids(df: pd.DataFrame) -> None:
    local_df = df.copy()
    authors = set(df['author1']).union(set(df['author2']))
    
    author_id_map = {}
    
    for i, author in enumerate(authors):
        author_id_map[author] = i
        
    df['author1'] = df['author1'].map(author_id_map)
    df['author2'] = df['author2'].map(author_id_map)