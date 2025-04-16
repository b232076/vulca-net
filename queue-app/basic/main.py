import cmd
from call_center import CallCenter

class CallCenterInterface(cmd.Cmd):
    intro = "Welcome to the Vulcanet Simulated Queue Application.\n"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.center = CallCenter(['A', 'B']) #Add 2 operators to the system

    def do_call(self, arg):#makes application receive a call whose id is <id>.
        self.center.receiveCall(arg.strip())

    def do_answer(self, arg): #makes operator <id> answer a call being delivered to it.
        self.center.answerCall(arg.strip())

    def do_reject(self, arg): #makes operator <id> reject a call being delivered to it.
        self.center.rejectCall(arg.strip())

    def do_hangup(self, arg): #makes call whose id is <id> be finished.
        self.center.hangupCall(arg.strip())

    def do_exit(self, arg):
        print("Exiting.")
        return True

if __name__ == "__main__":
    CallCenterInterface().cmdloop()