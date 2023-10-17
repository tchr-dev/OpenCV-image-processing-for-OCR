#!/bin/zsh

# Define the intermediate processed image directory
processed_dir="improved_images"

# Define the list of --oem options to test
oem_options=("1" "3")

# Define the list of --psm options to test
psm_options=("1" "2" "3" "4" "11" "12")

# Define the output directory for OCR results
output_dir="output"

# Create the directories if they don't exist
mkdir -p "$output_dir"

if [ -d $processed_dir ]; then
  for file in "$processed_dir"/*; do
    if [ -f "$file" ]; then 
        # Now, iterate through --oem and --psm options for OCR
        for oem in $oem_options; do
          for psm in $psm_options; do
            # Generate the output file name based on processing and OCR options
            output_file="${output_dir}/output_$(basename "$file")_oem${oem}_psm${psm}.txt"

            
            # Run Tesseract with the current options on the processed image
            tesseract "$file" "$output_file" -l chi_sim+eng --oem "$oem" --psm "$psm"
            
            # Print a message with the current options
            echo "OCR completed for $input_file with resize factor $resize_factor, option $option, --oem $oem, and --psm $psm. Output saved to $output_file"
          done
        done
      
    fi
  done
fi


echo "OCR testing completed."
