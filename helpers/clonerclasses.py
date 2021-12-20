'''Container classes for own collections'''

from dataclasses import dataclass, field

@dataclass
class Backup:
    '''Class to contain one backup info'''
    name: str = None
    remote_login: str = None
    remote_host: str = None
    remote_file: str = None
    target_folder: str = None
    target_file: str = None
    versions: int = 5


@dataclass
class CmdlineArguments:
    '''Class to contain command line arguments'''
    conf_file: str = None
    target_folder: str = None
    delete_old_versions: bool = True
    verbose: bool = False
    configtest: bool = False
    backup_names: dict = field(default_factory=dict)
    test: bool = False

@dataclass
class ConfigFile:
    '''Class to contain configuration file parameters'''
    log_file: str = None
    log_level: int = 0
    is_log_written: bool = False
    root_folder: str = None
