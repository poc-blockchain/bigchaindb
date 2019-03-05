import logging

# Create log instance to use across the module
log = logging.getLogger('asset')

# Create a console handler
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

log.setLevel(logging.INFO)
log.addHandler(ch)
