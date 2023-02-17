import logging
import constants

logger = logging.getLogger(constants.APPLICATION_NAME)
logging.basicConfig(format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
