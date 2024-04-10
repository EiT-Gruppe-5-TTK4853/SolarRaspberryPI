import logging
import threading
import subprocess


logging.basicConfig(
    filename="main.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def run_script(script_name):
    subprocess.run(["python", script_name])


if __name__ == "__main__":
    logging.info("The script is running.")
    t1 = threading.Thread(target=run_script, args=("battery_values.py",))
    t2 = threading.Thread(target=run_script, args=("api.py",))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
