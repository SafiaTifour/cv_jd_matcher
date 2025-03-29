import subprocess
import sys

def run_script(script_name):
    """Runs a Python script and checks for errors."""
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Running transform_to_json.py...")
    run_script("transform_to_json.py")
    
    print("Running similarity_ranking.py...")
    run_script("similarity_ranking.py")
    
    print("All scripts executed successfully!")
