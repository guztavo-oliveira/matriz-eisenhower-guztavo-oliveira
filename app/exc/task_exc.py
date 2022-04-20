class ValueOffRangeError(Exception):
    valid_options = {"importance": [1, 2], "urgency": [1, 2]}

    def __init__(self, importance, urgency):

        self.message = {
            "msg": {
                "valid options": self.valid_options,
                "received_options": {
                    "importance": importance,
                    "urgency": urgency,
                },
            },
        }
