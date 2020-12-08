import os
import yaml

from .logger import Logger

class CacheHandler:
    def __init__(self, project_dir, locales_path):
        self.locales_dir = os.path.join(project_dir, locales_path)


    def reset_cache(self):
        Logger.info('Cache reloading...')
        self.cache = {}

        for subdir, dirs, files in os.walk(self.locales_dir):
            for file in files:
                if file.lower().endswith('yml'):
                    file_name = os.path.join(subdir, file)

                    with open(file_name, encoding='utf-8') as stream:
                        locale = yaml.safe_load(stream)
                        self.add_to_cache(locale)

        Logger.info('Cache reloaded.')
        return self.cache


    def add_to_cache(self, locale, base_dict = None, origin = []):
        if base_dict is None:
            base_dict = self.cache

        for key in locale:
            if key in base_dict:
                current_origin = origin + [key]

                if isinstance(base_dict[key], dict) and isinstance(locale[key], dict):
                    self.add_to_cache(locale[key], base_dict = base_dict[key], origin = current_origin)
                elif base_dict[key] == locale[key]:
                    continue
                else:
                    Logger.warn('conflict:', '.'.join(current_origin))
            else:
                base_dict[key] = locale[key]
