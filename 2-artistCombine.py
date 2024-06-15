import pandas as pd


input_file_iran = 'csv-dir/release_iran.csv'
input_file_artist = 'csv-dir/release_artist.csv'
output_file_path = 'csv-dir/release_iran_artists.csv'

# Define the chunk size
chunksize = 10000


merged_df = pd.DataFrame()


iran_chunk_count = 0
artist_chunk_count = 0
total_merged_rows = 0


for chunk_iran in pd.read_csv(input_file_iran, chunksize=chunksize):
    iran_chunk_count += 1
    print(f"Processing Iran release chunk {iran_chunk_count} with {len(chunk_iran)} rows")


    for chunk_artist in pd.read_csv(input_file_artist, chunksize=chunksize):
        artist_chunk_count += 1
        print(f"Processing artist chunk {artist_chunk_count} with {len(chunk_artist)} rows")

        # Merge the chunks on id and release_id columns
        merged_chunk = pd.merge(chunk_iran, chunk_artist, left_on='id', right_on='release_id')
        merged_rows_count = len(merged_chunk)

        # Append the merged chunk to the DataFrame
        merged_df = pd.concat([merged_df, merged_chunk])
        total_merged_rows += merged_rows_count

        print(f"Merged chunk {iran_chunk_count}-{artist_chunk_count} with {merged_rows_count} rows")

merged_df.to_csv(output_file_path, index=False)

print(f"Merged data has been written to {output_file_path}")
print(f"Total merged rows: {total_merged_rows}")
