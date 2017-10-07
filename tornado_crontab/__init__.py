from ._crontab import CronTabCallback, crontab

__all__ = ["CronTabCallback", "crontab", "version", "version_info"]

version = "0.3.3"
version_info = tuple([int(v) for v in version.split(".")[:3]])
