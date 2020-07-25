def Save(file, content):
    f = open(file, "w")
    f.write(content)
    f.close()


def Read(file):
    f = open(file)
    fd = f.read()
    f.close()
    return fd


def getLogger(name):
    """
    :type name: str
    """
    import logging

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # add formatter to ch and add ch to logger
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.debug("Logger created")

    return logger
