## Installation Guide

Follow these steps to install and set up Genlingo on your system.

### Prerequisites

- Python 3.7 or above
- Pip package manager

### Step 1: Clone the Repository

Clone the Genlingo repository to your local machine:

```bash
git clone https://github.com/your-username/genlingo.git
```
### Step 2: Create and Activate a Virtual Environment

Create a new virtual environment for Genlingo:

```bash
python -m venv genlingo-env
```
Activate the virtual environment:

- On macOS and Linux:

```bash
source genlingo-env/bin/activate
```
- On Windows:

```bash
genlingo-env\Scripts\activate
```
### Step 3: Install Dependencies

Install the required dependencies listed in the `requirements.txt` file:
    
```bash
pip install -r requirements.txt
```

### Step 4: Install Additional Dependencies

Install the following additional dependencies:

#### Googletrans
```bash
pip install googletrans==4.0.0-rc1
```
#### ttkbootstrap
```bash
pip install ttkbootstrap
```
**Note**: If in this step you encounter an import error related to 
`_get_default_root`, you can comment out that line.

### Step 5: Run the Program

You're now ready to run Genlingo:

```bash
python genlingo.py
```

Make sure to activate the virtual environment (if not already) before running the program.

---

That's it! Genlingo is now installed and ready to use. Enjoy your language learning journey!

