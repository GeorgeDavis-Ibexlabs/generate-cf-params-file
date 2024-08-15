import logging
from random import randint

class ParameterTypeHandler:

    # ParameterTypeHandler Constructor
    # logger: Logger object
    #
    # Returns: ParameterTypeHandler object
    # Raises: None
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def _generate_substr(
        self,
        _alphabets: bool,
        _prefix: bool = False,
        _prefix_str: str = '',
        _num: bool = False,
        _hyphens: bool = False,
    ) -> str:
    
        built_str = ''

        if _prefix:
            built_str = _prefix_str
        if _alphabets:
            built_str += 'abcdef'
        if _hyphens:
            built_str += '-'
        if _num:
            built_str += '012345'
        
        return built_str

    def _generate_string(
        self,
        alphabets: bool,
        prefix: bool = False,
        prefix_str: str = '',
        num: bool = False,
        hyphens: bool = False,
        generate_list: bool = False,
        csv: bool = False
    ) -> str:

        from random import randint
        if generate_list:
            built_list = []
            for i in range(0, randint(0,3)):
                built_list.append(self._generate_substr(_alphabets=alphabets, _prefix=prefix, _prefix_str=prefix_str, _num=num, _hyphens=hyphens))
            return built_list
        elif csv:
            built_csv = ''
            for i in range(0, randint(0,3)):
                built_csv += self._generate_substr(_alphabets=alphabets, _prefix=prefix, _prefix_str=prefix_str, _num=num, _hyphens=hyphens) + ","
            return built_csv[:-1]
        else:
            return self._generate_substr(_alphabets=alphabets, _prefix=prefix, _prefix_str=prefix_str, _num=num, _hyphens=hyphens)

    # Generate pseudo parameter values based on parameter types 
    def generate_value_for_parameter_type(self, parameter_type: str) -> any:

        if parameter_type == "String":

            return self._generate_string(alphabets=True)

        elif parameter_type == "Number":

            return randint(0, 10)

        elif parameter_type == "AWS::EC2::Subnet::Id":

            return self._generate_string(alphabets=True, prefix=True, prefix_str='subnet-')

        elif parameter_type == "List<AWS::EC2::Subnet::Id>":

            return self._generate_string(alphabets=True, prefix=True, prefix_str='subnet-', num=True, generate_list=True)

        elif parameter_type == "AWS::EC2::SecurityGroup::Id":

            return self._generate_string(alphabets=True, prefix=True, prefix_str='sg-', num=True)

        elif parameter_type == "AWS::EC2::KeyPair::KeyName":

            return self._generate_string(alphabets=True, prefix=True, prefix_str='key-', num=True)

        elif parameter_type == "CommaDelimitedList":

            return self._generate_string(alphabets=True, num=True, csv=True)

        elif parameter_type == "AWS::EC2::VPC::Id":

            return self._generate_string(alphabets=True, prefix=True, prefix_str='vpc-', num=True)

        elif parameter_type == "AWS::Route53::HostedZone::Id":

            return self._generate_string(alphabets=True, num=True).upper()

        else:

            self.logger.debug("Unexpected parameter type " + str(parameter_type) + ". If the parameter type is a new or valid CloudFormation parameter type, please raise an issue with https://github.com/GeorgeDavis-Ibexlabs/generate-cf-params-file/issues to add it to the list of handled parameter types.")
            return "ToBeDetermined"
        
    
