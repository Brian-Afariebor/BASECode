type ErrorText = str
type HelpText = str

class PositionError(RuntimeError):

    NOTE: HelpText = (
        "All Positions are greater than 0,"
            +" and less than the amount of tokens"
        )

    def __init__(self, message: ErrorText):

        super().__init__(message)

        self.add_note(PositionError.NOTE)
    