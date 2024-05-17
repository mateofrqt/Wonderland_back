import pandas as pd

# Parameters
csv_file = "C:/Users/fourq/Downloads/dune-swaps-RAW.csv"
chunk_size = 100000


def process_chunk(chunk):
    # Convert amount0 to absolute values
    chunk["amount0"] = chunk["amount0"].abs()

    # Convert evt_block_time to datetime
    chunk["evt_block_time"] = pd.to_datetime(chunk["evt_block_time"], errors="coerce")

    # Extract the datetime up to the minute
    chunk["minute"] = chunk["evt_block_time"].dt.strftime("%Y-%m-%d %H:%M")

    # Group by the datetime minute and sum the amount0 values
    result = chunk.groupby("minute")["amount0"].sum().reset_index()

    # Debug: Print shape of the processed chunk result
    print(f"Processed chunk result shape: {result.shape}")

    return result


# Initialize an empty list to store the results
results = []

# Process CSV in chunks
for i, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunk_size)):
    print(f"Processing chunk {i + 1}, chunk shape: {chunk.shape}")
    processed_chunk = process_chunk(chunk)
    results.append(processed_chunk)

# Combine all the processed chunks into a single DataFrame
if results:
    final_results = pd.concat(results)
    # Group by minute again to handle any overlaps between chunks and sum amount0
    final_results = final_results.groupby("minute")["amount0"].sum().reset_index()

    # Debug: Print first few rows of final_results to verify final grouping
    print("Final results preview:")
    print(final_results.head())

    # Save the processed data to a new CSV file
    final_results.to_csv("summed_amount0_by_minute.csv", index=False)
else:
    print("No data processed.")
