from worker import run_worker

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    run_worker()
