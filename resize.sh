#!/bin/zsh

source .venv/bin/activate

# Define the input images directory
input_dir="images"

# Define the intermediate processed image directory
processed_dir="improved_images"

# Create the directories if they don't exist
mkdir -p "$processed_dir"

# Define the list of resize factors to test with main_cli.py
resize_factors=(1 1.5 2 3 4)

other_options=(    
    "--gaussian" 
    "--adaptive gaussian"
    "--adaptive mean"
    "--morph open"
    "--morph close"
    # "--sobel h"
    # "--sobel v"
    )

# Iterate through all images in the input directory
for input_file in "$input_dir"/*; do
    # Determine the base name of the input file
    base_name=$(basename "$input_file")

    # Iterate through resize factors
    for resize_factor in $resize_factors; do
        # Iterate through options
        for option in $other_options; do
            # Define the processed file path

            # processed_file="${processed_dir}/processed_${resize_factor}_${option_name}_${base_name}"
            new_options_array=("${(@s: :)option}")

            if (($#new_options_array == 1)); then
                # Combine the command and arguments
                cmd=("python" "main_cli.py" "--image" "$input_file" "--output" "$processed_dir" "--resize_factor" "$resize_factor" "$new_options_array[1]")
            elif (($#new_options_array == 2)); then
                cmd=("python" "main_cli.py" "--image" "$input_file" "--output" "$processed_dir" "--resize_factor" "$resize_factor" "$new_options_array[1]" "$new_options_array[2]")
            fi

            
            # Execute the command
            "${cmd[@]}"
            # echo "$cmd"

            # Print a message with the current processing options
            echo "Image $input_file processed with resize factor $resize_factor and option $option. Processed image saved to $processed_dir"
        done
    done
done
