import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s trace_id=%(trace_id)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
