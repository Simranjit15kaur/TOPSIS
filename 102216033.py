import sys    
import pandas as pd
import numpy as np

#Normalize the matrix
def normalization(data):
    columns = np.sqrt((data**2).sum(axis=0))
    normalized = data / columns
    return normalized

#Calculate ideal solutions
def ideal_sol(weighted_data, impacts):
    ideal_best = []
    ideal_worst = []

    for col, impact in zip(weighted_data.T, impacts):
        if impact == '+':  # Beneficial criterion
            ideal_best.append(max(col))
            ideal_worst.append(min(col))
        elif impact == '-':  # Non-beneficial criterion
            ideal_best.append(min(col))
            ideal_worst.append(max(col))
        else:
            raise ValueError("WRONG IMPACT: must be '+' or '-'")
    return np.array(ideal_best), np.array(ideal_worst)

#Calculate scores
def topsis(data, weights, impacts):
    normal_data = normalization(data)
    weighted_data = normal_data * weights
    ideal_best, ideal_worst = ideal_sol(weighted_data, impacts)

    # Euclidean distance
    best_distance = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
    worst_distance = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))
    scores = worst_distance / (best_distance + worst_distance)
    return scores

# Validate inputs
def validate_inputs(df, weights, impacts):
    # Ensure at least 3 columns exist
    if df.shape[1] < 3:
        raise ValueError("Input file must contain at least three columns.")
    
    # Ensure weights match the number of criteria columns
    num_criteria_columns = df.shape[1] - 1  # Exclude the first column
    if len(weights) != num_criteria_columns:
        raise ValueError(f"Number of weights ({len(weights)}) must match the number of criteria columns ({num_criteria_columns}).")
    
    # Ensure impacts match the number of criteria columns
    if len(impacts) != num_criteria_columns:
        raise ValueError(f"Number of impacts ({len(impacts)}) must match the number of criteria columns ({num_criteria_columns}).")
    
    # Ensure impacts are only '+' or '-'
    if not all(impact in ['+', '-'] for impact in impacts):
        raise ValueError("Impacts must be either '+' or '-'.")    


# Main function
def main():
    sys.argv = ["102216033.py", "102216033-data.csv", "1,1,1,2,1", "+,+,-,+,+"]

    if len(sys.argv) != 4:
        print("Usage: <set.py> <inputDataFile> <weights> <Impact> <ResultFileName>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    result_file = "102216033-result.csv"

    try:
        df = pd.read_csv(input_file)
        weights = list(map(float, weights_str.split(',')))
        impacts = impacts_str.split(',')

        # Validate inputs
        validate_inputs(df, weights, impacts)

        # Extract numerical data and calculate scores
        data = df.iloc[:, 1:].values.astype(float)
        scores = topsis(data, np.array(weights), impacts)

        # Add scores and ranks to the dataframe
        df['TOPSIS Score'] = scores
        df['Rank'] = df['TOPSIS Score'].rank(ascending=False).astype(int)

        # Saving the result to a CSV file
        df.to_csv(result_file, index=False)
        print(f"Result saved in {result_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
