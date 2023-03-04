
class CommandExecutable(object):
    _command_executable = {}

    @classmethod
    def command_task_done(cls, author) -> None:
        cls._command_executable[author] = True

    @classmethod
    def command_task_start(cls, author) -> None:
        cls._command_executable[author] = False

    @classmethod
    def chk_command_executable(cls, author) -> bool:
        if not author in cls._command_executable:
            return True
        return cls._command_executable[author]
