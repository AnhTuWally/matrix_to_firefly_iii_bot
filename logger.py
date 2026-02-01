import logging

def get_logger(name):
    log = logging.getLogger(name)

    if not log.hasHandlers():
        log.setLevel(logging.DEBUG)

    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    return log
