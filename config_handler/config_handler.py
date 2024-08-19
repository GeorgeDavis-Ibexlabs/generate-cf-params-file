from os import getcwd, environ, listdir
import logging
import traceback
import json

# The Config List - List of Config keys.
ConfigKeyList = [
    'exclude_folders'
]

class ConfigHandler():

    # ConfigHandler Constructor
    # logger: Logger object
    #
    # Returns: ConfigHandler object
    # Raises: None
    def __init__(self, logger: logging.Logger):

        # Create a JSON Config parser
        self.logger = logger
        self.config = self.get_combined_config()

    # Load the config.json file from the current working directory, or from the GITHUB_WORKSPACE environment variable if running inside GitHub Actions
    def __load_config_file(self) -> dict:

        try:
            package_dir = __file__.split(self.__module__.replace('.', '/'))[0]

            for file in listdir(package_dir):

                if file == 'config.json':

                    # Parse JSON Config
                    with open(package_dir + file, 'r') as config_file:

                        config_json = json.loads(config_file.read())

                        self.logger.debug('Config JSON key values found within ' + file + ' file - ' + str(config_json))
                        
                        return config_json
        
        except Exception as e:
            self.logger.error('Error loading config.json file: ' + str(traceback.print_tb(e.__traceback__)))

    # Load the config.json file from environment variables instead if running inside GitHub Actions. Environment variables override config.json values to enable CI workflows.
    def __load_config_env(self) -> dict:

        try:
            config = {}

            for config_key in ConfigKeyList:

                if config_key in environ.keys():

                    self.logger.debug('Config found within environment variables - ' + str(config_key))

                    config.update({config_key: environ.get(key = config_key).split(',')})

            self.logger.debug('Config from environment variables - ' + str(config))
            return config
        
        except Exception as e:
            self.logger.error('Error loading environment variables: ' + str(traceback.print_tb(e.__traceback__)))
            
    def get_combined_config(self) -> dict:
        from mergedeep import merge
        try:
            # Build a config file using config.json if it exists    
            config_file = self.__load_config_file()

            # Override config.json if exists, with Environment variables for CI purposes
            config_env = self.__load_config_env()

            # Return merged config objects
            return merge(config_file, config_env)

        except Exception as e:
            self.logger.error('Error merging config: ' + str(traceback.print_tb(e.__traceback__)))
        