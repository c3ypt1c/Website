def getLogger(name):
    """
    :type name: str
    """
    import logging

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # add formatter to ch and add ch to logger
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.debug("Basic Logger Config set")

    return logger
