AVBE = "available"
RING = "ringing"
BUSY = "busy"
class Operator: # Operator class for the call-center app

    def __init__(self, operator_id):
        self.id = operator_id
        self.state = AVBE  
        self.currentCall = None 

class Call:
    def __init__(self, call_id):
        self.id = call_id
        self.assignedOp = None
