from SocketServer import UDPServer, ThreadingMixIn, DatagramRequestHandler
import struct, socket, db

class Handler( DatagramRequestHandler ):
    def handle(self):
        data=self.request[0];
        socket=self.request[1];
        # length error
        if len(data) < 2:
            self.return1BData(1)
            return;
        src = ip2long( self.client_address[0] )
        sockType=struct.unpack("!B", data[0])[0]
        # type 1 is the ip list packet
        if sockType==1:
            ipNum = struct.unpack( "!B", data[1] )[0];
            # length error
            if len(data) < ipNum*4+2:
                self.return1BData(1)
                return;
            ipList=[]
            for i in range(ipNum):
                ip = struct.unpack( "!I", data[2+i*4:2+(i+1)*4] )[0]
                ipList.append(ip)
            db.UpdateIpMb(src, ipList)
            self.return1BData(0)
        
        # type 2 is the request
        if sockType==2:
            angle = 1;
            if len(data) == 5:
                dstIp = struct.unpack( "!I", data[1:] )[0]
                dstMb = db.FindMb(dstIp);
                angle = db.FindRoute( src, dstMb)
            # socket.sendto( struct.pack( "!B", angle ), self.client_address )
            self.return1BData( angle )
            
            
    def return1BData(self, data):
        self.request[1].sendto( struct.pack("!B",data), self.client_address )
            

class Server( ThreadingMixIn, UDPServer ):
    pass 

host='192.168.1.52'
port=7890

def ip2long (ip):
    '''change the string format ip to unsigned long format'''
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def long2ip (lint):
    '''change the unsingned long format ip to string format'''
    return socket.inet_ntoa(struct.pack("!I", lint))

if __name__ == "__main__":
    addr=(host,port)
    server=Server( addr, Handler )
    server.serve_forever()