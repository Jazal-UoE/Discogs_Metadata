import pandas as pd


input_file_path = 'csv-dir/release_iran_artists_combined.csv'


df = pd.read_csv(input_file_path)

# Initialize counters
total_songs = len(df)
songs_with_composer = df['composer_name'].notna().sum()
songs_with_lyricist = df['lyricist_name'].notna().sum()
songs_with_composer_and_lyricist = df['composer_name'].notna() & df['lyricist_name'].notna()

# Calculate the number of unique composers and lyricists
unique_composers = pd.Series(df['composer_name'].dropna().str.split(', ').sum()).unique()
unique_lyricists = pd.Series(df['lyricist_name'].dropna().str.split(', ').sum()).unique()

print("\nDetailed Breakdown:")
print(f"Total number of songs: {total_songs}")
print(f"Number of songs with composer information: {songs_with_composer}")
print(f"Number of songs with lyricist information: {songs_with_lyricist}")
print(f"Number of songs with both composer and lyricist information: {songs_with_composer_and_lyricist.sum()}")

print(f"Number of unique composers: {len(unique_composers)}")
print(f"Number of unique lyricists: {len(unique_lyricists)}")

detailed_df = df[['release_id', 'title', 'composer_name', 'lyricist_name']]
detailed_df = detailed_df[detailed_df['composer_name'].notna() | detailed_df['lyricist_name'].notna()]

