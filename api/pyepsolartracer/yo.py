import time

def print_hello():
    while True:
        print("Hello")
        time.sleep(10)  # Wait for 10 seconds

if __name__ == "__main__":
    input("Press Enter to start printing 'Hello' every 10 seconds...")
    print_hello()
