import pandas as pd


input_file_path = 'csv-dir/release.csv'
output_file_path = 'csv-dir/release_iran.csv'

# Define the chunk size
chunksize = 10000
filtered_df = pd.DataFrame()
chunk_count = 0
iran_found = False

for chunk in pd.read_csv(input_file_path, chunksize=chunksize):

    chunk_count += 1
    chunk_filtered = chunk[chunk['country'] == 'Iran']


    if not chunk_filtered.empty:
        iran_found = True


    filtered_df = pd.concat([filtered_df, chunk_filtered])
    print(f"Processed chunk {chunk_count}, Iran found: {'Yes' if not chunk_filtered.empty else 'No'}")


filtered_df.to_csv(output_file_path, index=False)

if iran_found:
    print(f"Filtered data has been written to {output_file_path}")
else:
    print("No rows with country value 'Iran' were found.")
