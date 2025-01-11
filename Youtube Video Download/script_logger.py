# script_logger.py

from datetime import datetime
import logging
import os
import inspect

# Initialize the script's start time when the module is imported
begin_time = datetime.now()


def log_message(message="", total_duration=False, script_name=False, device="", type="info"):
    """
    Logs and prints a formatted message with current time, input string, 
    and optionally calculates total duration if begin_time is provided.

    Parameters:
    - message (str): The message to be logged and printed.
    - begin_time (datetime, optional): The starting time of an event.
    - total_duration (bool, optional): If True, calculates the total duration.
    - script_name (bool, optional): If True, includes the script name in the log.
    """

    # Initialize the logging file and initial output
    if message == "" and type == "info" and not total_duration and not script_name:
        script_name = True
        message = "Script Initialization"
        # Use inspect to find the caller's filename
        caller_frame = inspect.stack()[1]
        caller_filename = os.path.splitext(os.path.basename(caller_frame.filename))[0]

        # Replace invalid characters in the timestamp for the filename
        formatted_time = begin_time.strftime("%Y-%m-%d_%H-%M-%S")

        if device.lower() == "laptop" or device.lower() == "":
            folder_path = "C:/Professional"
        elif device.lower() == "desktop":
            folder_path = "A:/Professional"
        elif device.lower() == "server" or device.lower() == "ubuntu":
            folder_path = "/home/ubuntu"

        # Configure logging with the script name and log file location
        logging.basicConfig(
            filename=f'{folder_path}/Presearch/Logs/{caller_filename} - {formatted_time}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    current_time = datetime.now()
    duration_text = ""

    # Get the name of the running script if script_name is requested
    if script_name:
        # Use inspect to find the caller's filename
        script_frame = inspect.stack()[1]
        script_filename = os.path.splitext(os.path.basename(script_frame.filename))[0]
        script_filename = f"- {script_filename}"
    else:
        script_filename = ""

    # Calculate total duration if total_duration is requested
    if total_duration:
        duration = current_time - begin_time
        duration_text = f"- Total Duration: {duration}"
    else:
        duration_text = ""

    # Format text
    log_text = f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} {script_filename} - {message} {duration_text}"

    # Output Text
    if type.lower() == "warning":
        logging.warning( log_text )
    elif type.lower() == "error":
        logging.error( log_text )
    elif type.lower() == "critical":
        logging.critical( log_text )
    else:
        logging.info(log_text)
    print(log_text)
    return log_text
