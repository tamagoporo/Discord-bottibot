
class ExecutableManager(object):
    _executable = {}

    @classmethod
    def task_done(cls, author) -> None:
        cls._executable[author] = True

    @classmethod
    def task_start(cls, author) -> None:
        cls._executable[author] = False

    @classmethod
    def chk_executable(cls, author) -> bool:
        if not author in cls._executable:
            return True
        return cls._executable[author]
