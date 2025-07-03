# bro

# Clone the repo into the current directory
git clone https://github.com/beenjaminAM/bro.git .

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

# Install the required package
pip install pymupdf

# (Optional) Upgrade pip
python -m pip install --upgrade pip

# Run your Python script
python .\clean_pdf.py