from twisted.internet import protocol, reactor
import json
from call_center_same import CallCenter

#Protocol that handles communication with each connected client
class CallCenterProtocol(protocol.Protocol):
    def connectionMade(self):
        """
        Called when a new client connects to the server.
        Adds the client to the list of active connections.
        """
        self.factory.clients.append(self)
        print(f"Client connected from {self.transport.getPeer()}")

    def dataReceived(self, data):
        """
        Called whenever data is received from the client.
        Parses the JSON command, delegates to the CallCenter logic, and sends back the response.
        """
        try:
            command = json.loads(data.decode())
            response = self.factory.center.handle_command(command)
            self.transport.write(json.dumps({"response": response}).encode())
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.transport.write(json.dumps({"response": error_msg}).encode())

    def connectionLost(self, reason):
        """
        Called when the client disconnects.
        Removes the client from the active list.
        """
        self.factory.clients.remove(self)
        print("Client disconnected")


# Factory that creates a new Protocol instance for each client connection
class CallCenterFactory(protocol.Factory):
    def __init__(self):
        #CallCenter instance manages the queue and operator logic
        self.center = CallCenter(['A', 'B'])
        #List of all currently connected clients
        self.clients = []

    def buildProtocol(self, addr):
        """
        Called for each new client connection.
        Returns a new instance of CallCenterProtocol.
        """
        proto = CallCenterProtocol()
        proto.factory = self  #Give protocol access to the factory (and the CallCenter)
        return proto


if __name__ == "__main__":
    #Start listening on TCP port 5678 and initialize the CallCenter server
    print("Starting Call Center server on port 5678...")
    reactor.listenTCP(5678, CallCenterFactory())  #Binds the factory to the port
    reactor.run()  #Starts the Twisted event loop and waits for events (blocking)
