import pandas as pd


input_file_path = 'csv-dir/release_iran_artists.csv'
output_file_path = 'csv-dir/release_iran_artists_roles.csv'

# Define the chunk size
chunksize = 10000
filtered_rows = []
chunk_count = 0
total_rows_processed = 0
total_filtered_rows = 0



def determine_song_role(row):
    roles = []

    if str(row['extra']) == '0':
        roles.append('Singer')

    role_value = str(row['role']).lower().replace(' ', '') if pd.notna(row['role']) else ''

    if 'compose' in role_value:
        roles.append('Composer')

    if 'lyric' in role_value:
        roles.append('Lyricist')

    return ', '.join(roles)


for chunk in pd.read_csv(input_file_path, chunksize=chunksize, dtype={'extra': str}):
    chunk_count += 1
    chunk_size = len(chunk)
    total_rows_processed += chunk_size

    # Apply the function to each row and filter the rows
    chunk['song_role'] = chunk.apply(determine_song_role, axis=1)
    filtered_chunk = chunk[chunk['song_role'] != '']

    filtered_rows.append(filtered_chunk)
    filtered_rows_count = len(filtered_chunk)
    total_filtered_rows += filtered_rows_count

    print(f"Processed chunk {chunk_count} with {chunk_size} rows; "
          f"Filtered {filtered_rows_count} rows; "
          f"Total rows processed: {total_rows_processed}; "
          f"Total filtered rows: {total_filtered_rows}")

# Concatenate all filtered chunks into a single DataFrame
filtered_df = pd.concat(filtered_rows, ignore_index=True)

# Select the relevant columns
output_df = filtered_df[['release_id', 'title', 'artist_id', 'artist_name', 'song_role']]
output_df.to_csv(output_file_path, index=False)

print(f"Processed data has been written to {output_file_path}")

# Debugging: Check a sample of the filtered DataFrame
print(filtered_df.head())
