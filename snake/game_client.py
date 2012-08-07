import cPickle
from threading import Thread
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from snake import Snake  
  
class GameClient(LineReceiver):
  end = "DEAD"
  
  def connectionMade(self):
    print("Connection made")

  def lineReceived(self, line):
    print "receive:", line
    if line==self.end:
      self.transport.loseConnection()

class GameClientFactory(ClientFactory):
  protocol = GameClient

  def clientConnectionFailed(self, connector, reason):
    print 'connection failed:', reason.getErrorMessage()
    reactor.stop()

  def clientConnectionLost(self, connector, reason):
    print 'connection lost:', reason.getErrorMessage()
    reactor.stop()