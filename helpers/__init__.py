'''Module containing different helper scripts / functions'''
from .logger import Logger

from .validator import ValidatorResult
from .validator import backup_name

from .filesystemchecks import is_folder_writable
from .filesystemchecks import folder_exists
from .filesystemchecks import file_exists
from .filesystemchecks import is_file_writable
from .filesystemchecks import get_files_folder