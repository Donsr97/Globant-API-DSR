import logging
import time

log = logging.getLogger("custom_logger")
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        log.info(f"Starting execution of {func.__name__}...")
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        execution_time = end_time - start_time
        log.info(f"Execution of {func.__name__} completed in {execution_time:.4f} seconds.")
        
        return result
    return wrapper
