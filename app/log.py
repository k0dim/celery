import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s : %(name)s : %(levelname)s : %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)