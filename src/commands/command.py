import abc


class Command:
    """
    Abstract base class for a command.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self):
        """
        Invokes the command
        :return:
            {
                'result': {},
                'error': {
                    'errored': False,
                },
            }
        """
        raise Exception('No execute')
