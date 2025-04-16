from operator_mod import Operator, Call
from collections import deque

class CallCenter:
    def __init__(self, operator_ids):
        # Create operator instances indexed by their IDs
        self.operators = {op_id: Operator(op_id) for op_id in operator_ids}
        # FIFO queue for incoming calls waiting to be assigned
        self.queue = deque()
        # Dictionary mapping call IDs to active Call instances
        self.activeCalls = {}

    def receiveCall(self, call_id):
        """
        Handles a new incoming call. If there is an available operator,
        the call is delivered immediately; otherwise, it's placed in the queue.
        """
        print(f"Call {call_id} received")
        call = Call(call_id)
        self.activeCalls[call_id] = call

        for operator in self.operators.values():
            if operator.state == "available":
                self.ring(operator, call)
                return

        print(f"Call {call_id} waiting in queue")
        self.queue.append(call)

    def ring(self, operator, call):
        """
        Delivers a call to an available operator by setting their state to 'ringing'
        and assigning the call to them.
        """
        operator.state = "ringing"
        operator.currentCall = call
        call.assignedOp = operator
        print(f"Call {call.id} ringing for operator {operator.id}")

    def answerCall(self, operator_id):
        """
        Called when an operator answers a ringing call.
        Changes their state to 'busy'.
        """
        operator = self.operators[operator_id]
        if operator.state == "ringing" and operator.currentCall:
            operator.state = "busy"
            print(f"Call {operator.currentCall.id} answered by operator {operator.id}")

    def rejectCall(self, operator_id):
        """
        Called when an operator rejects a ringing call.
        The call will be redelivered to another available operator if possible.
        """
        operator = self.operators[operator_id]
        if operator.state == "ringing" and operator.currentCall:
            call = operator.currentCall
            operator.state = "available"
            operator.currentCall = None
            print(f"Call {call.id} rejected by operator {operator.id}")
            self.tryRedeliver(call)

    def hangupCall(self, call_id):
        """
        Called when a caller hangs up.
        Frees the operator if the call was in progress or ringing.
        Removes the call from the queue if it had not yet been delivered.
        """
        call = self.activeCalls.get(call_id)
        if not call:
            return

        operator = call.assignedOp

        if operator:
            if operator.state == "busy":
                # The call was in progress
                operator.state = "available"
                operator.currentCall = None
                print(f"Call {call.id} finished and operator {operator.id} available")
                self.activeCalls.pop(call_id)
                self.checkQueue()
            elif operator.state == "ringing":
                # The call was ringing but not answered
                print(f"Call {call.id} missed")
                operator.state = "available"
                operator.currentCall = None
                self.activeCalls.pop(call_id)
                self.checkQueue()
            else:
                # The call was already marked as handled
                print(f"Call {call.id} missed")
                self.activeCalls.pop(call_id)
        else:
            # The call was never assigned and still in queue
            print(f"Call {call.id} missed")
            if call in self.queue:
                self.queue.remove(call)
            self.activeCalls.pop(call_id)

    def checkQueue(self):
        """
        Checks the queue for waiting calls and assigns the next one
        to the first available operator (FIFO).
        """
        if self.queue:
            for operator in self.operators.values():
                if operator.state == "available":
                    call = self.queue.popleft()
                    self.ring(operator, call)
                    break

    def tryRedeliver(self, call):
        """
        Attempts to deliver a rejected call to another available operator.
        If no operator is available, the call is placed back in the queue.
        """
        for operator in self.operators.values():
            if operator.state == "available":
                self.ring(operator, call)
                return
        self.queue.append(call)
