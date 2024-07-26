import logging
import os
from logstash_async.handler import AsynchronousLogstashHandler

# def setup_logger():
#     host = "logstash"
#     port = 5000
#     logger_name = "python-logstash-logger"
#     database_path = ""  # Adjust or specify the correct path

#     # Check environment for log mode
#     log_mode = os.getenv("LOG_MODE", "logstash").lower()

#     # Create the logger
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(logging.INFO)

#     if log_mode == "console":
#         # Create console handler
#         handler = logging.StreamHandler()
#         print("Logging mode set to console.")
#     else:
#         # Create Logstash handler
#         handler = AsynchronousLogstashHandler(host, port, database_path)
#         print("Logging mode set to Logstash.")
    
#     # Create the formatter and set it to the handler
#     formatter = logging.Formatter(
#         "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#         )
#     handler.setFormatter(formatter)

#     # Add the handler to the logger
#     logger.addHandler(handler)
#     return logger

# logger = setup_logger()

def setup_logger():
    logmode = os.getenv("LOG_MODE", "logstash").lower()

    if logmode == "console":
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
    else:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        host = "logstash"
        port = 5000
        logger_name = "python-logstash-logger"
        database_path = ""
        handler = AsynchronousLogstashHandler(host, port, database_path)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


logger = setup_logger()