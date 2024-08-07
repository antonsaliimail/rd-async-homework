# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r lesson_2/requirements.txt

# Navigate to the lesson_2 folder
cd lesson_2

# Start the script with the --file <path_to_your_file.txt>
python main.py --file example_input.txt

# The results are saved to the lesson_2/downloaded_data dir