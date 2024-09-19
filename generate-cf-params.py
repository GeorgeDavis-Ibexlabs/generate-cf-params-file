#! /usr/bin/env python3
from os import environ, walk
import logging
from cfn_tools import load_yaml

# Setting up the logging level from the environment variable `LOGLEVEL`.
if 'LOG_FILENAME' in environ.keys():
    logging.basicConfig(
        filename=environ['LOG_FILENAME'],
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S'
    )
    logger = logging.getLogger(__name__)
else:
    logging.basicConfig()
    logger = logging.getLogger(__name__)

logger.setLevel(environ['LOG_LEVEL'] if 'LOG_LEVEL' in environ.keys() else 'INFO')

from parameter_type_handler.parameter_type_handler import ParameterTypeHandler
parameter_type_handler = ParameterTypeHandler(logger=logger)

from config_handler.config_handler import ConfigHandler

config_handler = ConfigHandler(logger=logger)
logger.debug("Combined config - " + str(config_handler.config))

file_paths = []

# list_yaml_files: Creates a list of YAML files recursively within current directory and nested directories within the current directory, returns a list of YAML files
def list_yaml_files(start_path: str) -> list:

    for path, _, files in walk(start_path):

        for f in files:

            file_paths.append(str(path) + "/" + str(f))

    yaml_files = []

    for file_path in file_paths:
        
        f_arr = file_path.split('/')

        if '.' not in f_arr[1][0]:

            if "exclude_folders" in config_handler.config:
                
                if f_arr[1] not in config_handler.config["exclude_folders"] and ( ".yml" in f_arr[-1] or ".yaml" in f_arr[-1] ):

                    yaml_files.append(file_path)

            elif ".yml" in f_arr[-1] or ".yaml" in f_arr[-1]:

                yaml_files.append(file_path)

    return yaml_files

# do_parameters_exist: Oh yes, they do! This function checks for strings like  "Parameters" and "Resources" within a YAML file, returns a list of likely AWS CloudFormation YAML files with Parameters defined within them
def do_parameters_exist(yaml_files_list: list) -> list:

    _yaml_files_with_parameters_list = []
    for file in yaml_files_list:
        
        logger.debug("YAML config file - " + str(file))
        with open(file, 'r') as f:
            
            file_content = f.read()

            logger.debug("File : " + str(file))

            # Resources is a mandatory section on AWS CloudFormation templates and hence increases the likelihood of a file that has "Parameters" and "Resources" in it to be a CloudFormation template
            if "Parameters" in file_content and "Resources" in file_content:

                _yaml_files_with_parameters_list.append(file)

    return _yaml_files_with_parameters_list

# Generate pseudo parameter values for identified parameter keys within the CloudFormation (YAML) files
def generate_pseudo_parameter_values(_yaml_files_with_parameters_list: list):
    
    from random import randint

    params_list = []
    _temp_params_key_list = []

    for file in _yaml_files_with_parameters_list:
        
        logger.debug("Found YAML file with Parameters - " + str(file))
        with open(file, 'r') as f:
            
            data = load_yaml(f)

            for item in data.items():

                if "Parameters" in item:

                    for element in item:

                        if element != "Parameters":

                            for elem in element:

                                elem_value = None

                                # If Default is provided, use Default value
                                if "Default" in element[elem]:

                                    elem_value = element[elem]["Default"]

                                # If AllowedValues are provided, assign a random allowed value
                                elif "AllowedValues" in element[elem]:

                                    elem_value = element[elem]["AllowedValues"][randint(0, len(element[elem]["AllowedValues"])-1)]

                                else:

                                    elem_value = parameter_type_handler.generate_value_for_parameter_type(parameter_type=element[elem]["Type"])

                                if elem not in _temp_params_key_list:
                                    
                                    _temp_params_key_list.append(elem)
                                    params_list.append({ elem: elem_value})

                                else:
                                    logger.warn("Repeat parameter key(s) found - " + elem)

    return params_list

def build_parameter_json_file(params_list: list) -> None:

    if params_list:

        param_list_str = ''
        for param in params_list:

            for item in param:

                param_list_str += "\"" + str(item) + "=" + str(param[item]) + "\","

        if param_list_str[-1] == ",":

            param_list_str = param_list_str[:-1]
        
        with open('params.json', 'w+') as params:
            
            params.write("[" + param_list_str + "]")

    else:
        logger.error("Error: The params.json file could not be generated. No pseudo parameters were generated.")
        raise Exception("Error: The params.json file could not be generated. No pseudo parameters were generated.")
            
if __name__ == '__main__':
    
    files_list = list_yaml_files('.')
    logger.info("Identified " + str(len(files_list)) + " YAML files")

    # if files_list:

    #     yaml_files_with_parameters_list = do_parameters_exist(yaml_files_list = files_list)
    #     logger.info(str(len(yaml_files_with_parameters_list)) + " out of " + str(len(files_list)) + " are likely to be AWS CloudFormation files")

    #     params_list = generate_pseudo_parameter_values(_yaml_files_with_parameters_list = yaml_files_with_parameters_list)

    #     build_parameter_json_file(params_list = params_list)