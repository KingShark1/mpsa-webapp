from application import Athletes
from util import utils

output = Athletes.query.all()
utils.update_event_dict(output[0])