import os

WHEEL_HOUSE = "/Users/julianbaumgartner/Library/Caches/pip/wheels"

if __name__ == "__main__":
    for root, dirs, files in os.walk(WHEEL_HOUSE):
        for file in files:
            if file.endswith(".whl"):
                print(file)
