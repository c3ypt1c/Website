import HelperFunctions

localLogger = HelperFunctions.getLogger()

# Set variables for generation
generateDownContent = True
generateODF = True

try:
    from odf import opendocument, text
except ModuleNotFoundError:
    localLogger.error("ODF documents will not be processed. Errors will occur if the program comes across such file")
    localLogger.error("Please install odfpy. Instructions: https://pypi.org/project/odfpy/")

try:
    from datauri import DataURI
except ModuleNotFoundError:
    generateDownContent = False
    localLogger.warning("Content for download will not be generated.")
    localLogger.warning("Please install python-datauri. Instructions: https://pypi.org/project/python-datauri/")

localLogger.debug("Loaded imports")
