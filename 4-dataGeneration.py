import pandas as pd
from collections import defaultdict


input_file_path = 'csv-dir/release_iran_artists_roles.csv'
output_file_path = 'csv-dir/songs_ir.csv'

# Define the chunk size
chunksize = 10000

# Initialize a dictionary to store the combined rows
combined_data = defaultdict(lambda: {
    'title': None,
    'singer_name': [],
    'singer_id': [],
    'composer_name': [],
    'composer_id': [],
    'lyricist_name': [],
    'lyricist_id': []
})

# Initialize counters for processed chunks and rows
chunk_count = 0
total_rows_processed = 0

# Read the input CSV file in chunks
for chunk in pd.read_csv(input_file_path, chunksize=chunksize):
    chunk_count += 1
    chunk_size = len(chunk)
    total_rows_processed += chunk_size

    # Process each row in the chunk
    for index, row in chunk.iterrows():
        release_id = row['release_id']
        title = row['title']
        artist_id = row['artist_id']
        artist_name = row['artist_name']
        song_role = row['song_role']

        if combined_data[release_id]['title'] is None:
            combined_data[release_id]['title'] = title

        if 'Singer' in song_role:
            combined_data[release_id]['singer_id'].append(artist_id)
            combined_data[release_id]['singer_name'].append(artist_name)

        if 'Composer' in song_role:
            combined_data[release_id]['composer_id'].append(artist_id)
            combined_data[release_id]['composer_name'].append(artist_name)

        if 'Lyricist' in song_role:
            combined_data[release_id]['lyricist_id'].append(artist_id)
            combined_data[release_id]['lyricist_name'].append(artist_name)

    print(f"Processed chunk {chunk_count} with {chunk_size} rows; "
          f"Total rows processed: {total_rows_processed}")

# Convert the combined data to a DataFrame
combined_df = pd.DataFrame([{
    'release_id': release_id,
    'title': data['title'],
    'singer_name': ', '.join(data['singer_name']),
    'singer_id': ', '.join(map(str, data['singer_id'])),
    'composer_name': ', '.join(data['composer_name']),
    'composer_id': ', '.join(map(str, data['composer_id'])),
    'lyricist_name': ', '.join(data['lyricist_name']),
    'lyricist_id': ', '.join(map(str, data['lyricist_id']))
} for release_id, data in combined_data.items()])


combined_df.to_csv(output_file_path, index=False)
print(f"Processed data has been written to {output_file_path}")

# Debugging: Check a sample of the combined DataFrame
print(combined_df.head())
