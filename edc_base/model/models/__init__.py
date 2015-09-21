from django import get_version

from .base_list_model import BaseListModel
from .base_model import BaseModel
from .base_uuid_model import BaseUuidModel

if not get_version().startswith('1.6'):
    from .historical_records import HistoricalRecords
