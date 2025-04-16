import json
from twisted.internet import protocol, reactor, stdio
from twisted.protocols import basic
from cmd import Cmd
#TCP Client with Twisted + CMD 
# This client will be responsible for reading user commands and communicating with the server.

class CmdInterpreter(Cmd):
    """
    Command-line interface that processes user commands and sends them to the server as JSON.
    """

    prompt = "" 

    def __init__(self, transport):
        """Send a 'call' command with the given call ID."""
        super().__init__()
        self.transport = transport

    def do_call(self, arg):
        """Send a 'call' command with the given call ID."""
        self.send_command("call", arg)

    def do_answer(self, arg):
        """Send an 'answer' command with the given operator ID."""
        self.send_command("answer", arg)

    def do_reject(self, arg):
        """Send a 'reject' command with the given operator ID."""
        self.send_command("reject", arg)

    def do_hangup(self, arg):
        """Send a 'hangup' command with the given call ID."""
        self.send_command("hangup", arg)

    def do_exit(self, arg):
        """Exit the client application gracefully."""
        print("Exiting...")
        self.transport.loseConnection()
        return True

    def default(self, line):
        """Handle invalid or unknown commands."""
        print("Invalid command.")

    def send(self, command, id_):
        """Convert a command and ID to JSON and send it to the server."""
        try:
            msg = {"command": command, "id": id_}
            self.transport.write(json.dumps(msg).encode())
        except Exception as e:
            print("Failed to send command:", e)


class StdioClient(basic.LineReceiver):
    """
    Twisted LineReceiver to handle user input from stdin line by line.
    Each line is passed to the CmdInterpreter.
    """

    delimiter = b'\n'  #Lines are delimited by newline characters
    
    def __init__(self, network_transport):
        self.cmd = CmdInterpreter(network_transport)

    def lineReceived(self, line):
        #Decode the input line from bytes and pass it to CmdInterpreter
        line = line.decode().strip()
        self.cmd.onecmd(line)



class QueueClient(protocol.Protocol):
    """
    Client protocol that connects to the server and sets up stdin for command input.
    """
    def connectionMade(self):
        #Inform the user and initialize stdin input handling
        print("Connected to server.\nYou may type: call <id>, answer <id>, reject <id>, hangup <id>")
        stdio.StandardIO(StdioClient(self.transport))

    def dataReceived(self, data):
        #Receive server response and print it
        try:
            response = json.loads(data.decode())
            print(response["response"])
        except Exception as e:
            print("Failed to decode server response:", e)


class QueueClientFactory(protocol.ClientFactory):
    """
    Factory to create QueueClient connections and handle connection loss or failure.
    """
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()

    def buildProtocol(self, addr):
        return QueueClient()


if __name__ == "__main__":
    #Start the client and connect to the server at localhost:5678
    reactor.connectTCP("localhost", 5678, QueueClientFactory())
    reactor.run()
