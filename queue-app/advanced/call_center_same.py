from operator_same_mod import Operator, Call
from collections import deque

class CallCenter:
    def __init__(self, operator_ids):
        self.operators = {op_id: Operator(op_id) for op_id in operator_ids}
        self.queue = deque()
        self.activeCalls = {}

    def handle_command(self, command): # Receives and interpret commands from client with JSON
        cmd = command.get("command")
        call_or_op_id = command.get("id")

        if cmd == "call":
            return self.receiveCall(call_or_op_id)
        elif cmd == "answer":
            return self.answerCall(call_or_op_id)
        elif cmd == "reject":
            return self.rejectCall(call_or_op_id)
        elif cmd == "hangup":
            return self.hangupCall(call_or_op_id)
        else:
            return f"Unknown command: {cmd}"

    def receiveCall(self, call_id):
        call = Call(call_id)
        self.activeCalls[call_id] = call
        for operator in self.operators.values():
            if operator.state == "available":
                return f"Call {call_id} received\n" + self.ring(operator, call)
        self.queue.append(call)
        return f"Call {call_id} received\nCall {call_id} waiting in queue"

    def ring(self, operator, call):
        operator.state = "ringing"
        operator.currentCall = call
        call.assignedOp = operator
        return f"Call {call.id} ringing for operator {operator.id}"

    def answerCall(self, operator_id):
        operator = self.operators[operator_id]
        if operator.state == "ringing" and operator.currentCall:
            operator.state = "busy"
            return f"Call {operator.currentCall.id} answered by operator {operator.id}"
        return f"No ringing call to answer for operator {operator_id}"

    def rejectCall(self, operator_id):
        operator = self.operators[operator_id]
        if operator.state == "ringing" and operator.currentCall:
            call = operator.currentCall
            operator.state = "available"
            operator.currentCall = None
            return f"Call {call.id} rejected by operator {operator.id}\n" + self.tryRedeliver(call)
        return f"No ringing call to reject for operator {operator_id}"

    def hangupCall(self, call_id):
        call = self.activeCalls.get(call_id)
        if not call:
            return f"Call {call_id} not found"

        operator = call.assignedOp
        response = f"Call {call.id} missed"

        if operator:
            if operator.state == "busy":
                operator.state = "available"
                operator.currentCall = None
                response = f"Call {call.id} finished and operator {operator.id} available\n" + self.checkQueue()
            elif operator.state == "ringing":
                operator.state = "available"
                operator.currentCall = None
                response = f"Call {call.id} missed\n" + self.checkQueue()
        elif call in self.queue:
            self.queue.remove(call)

        self.activeCalls.pop(call_id, None)
        return response

    def checkQueue(self):
        if self.queue:
            for operator in self.operators.values():
                if operator.state == "available":
                    call = self.queue.popleft()
                    return self.ring(operator, call)
        return ""

    def tryRedeliver(self, call):
        for operator in self.operators.values():
            if operator.state == "available":
                return self.ring(operator, call)
        self.queue.append(call)
        return f"Call {call.id} waiting in queue"
