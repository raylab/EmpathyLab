import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import sqlite3
import json
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 
''' 

myDB = '3ff7725c-3326-4519-aef5-4c6f92337d13.db'
conn = sqlite3.connect(myDB)
c = conn.cursor()
c.execute('SELECT * from "dump"')
dumpRows = c.fetchall()

#c.execute('SELECT * from "frame"')

frame_headers = ["DUMP_ID", "COUNTER", "INTERPOLATED", "RAW_CQ", \
           "AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2", \
           "P8", "T8", "FC6", "F4", "F8", "AF4", "GYROX", "GYROY", \
           "TIMESTAMP", "MARKER_HARDWARE", "ES_TIMESTAMP", "FUNC_ID", \
           "FUNC_VALUE", "MARKER", "SYNCSIGNAL"]
dump_headers = ["ID", "TIMESTAMP", "USERID", "RECORDNUMBER"]
eq_headers = ["DUMP_ID", "IEE_CHAN_CMS", "IEE_CHAN_DRL", "IEE_CHAN_FP1", \
              "IEE_CHAN_AF3", "IEE_CHAN_F7", "IEE_CHAN_F3", "IEE_CHAN_FC5", \
              "IEE_CHAN_T7", "IEE_CHAN_P7", "IEE_CHAN_O1", "IEE_CHAN_O2", \
              "IEE_CHAN_P8", "IEE_CHAN_T8", "IEE_CHAN_FC6", "IEE_CHAN_F4", \
              "IEE_CHAN_F8", "IEE_CHAN_AF4", "IEE_CHAN_FP2",]
myRows = c.fetchall()

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
        #self.write_message("B13\r")
        #Do_rows(self, 0)
        Get_time(self, 0)
      
    def on_message(self, message):
        print ('message received:  %s' % message)
        sync = int(message) + 1
        #Do_rows(self, sync)
        Get_time(self, sync)

    def on_send(self, message):
        self.write_message(message)
 
    def on_close(self): 
        print ('connection closed')
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])

def Get_time(obj, z):
    ids = []
    row = dumpRows[z]
    
    #for i, row in enumerate(dumpRows) :
    if z < len(dumpRows):
        if row[1] == dumpRows[z+1][1] :
            print("Getting time", row[1], dumpRows[z+1][1])# dumpRows))
            ids.append(row[0])
        elif row[1] < dumpRows[z+1][1] :
            ids.append(row[0])
            c.execute('SELECT * from "frame" where DUMP_ID between %s and %s' %(ids[0],ids[len(ids)-1]))
            frameRows = c.fetchall()
            myStrA = {}
            myList = []
            for frame in frameRows:
                myStr = {}
                for a, val in enumerate(frame):
                    myStr[frame_headers[a]] = val
                myList.append(myStr)
            myStrA['frames'] = myList
            myStrA['number'] = z
            myStr = json.dumps(myStrA)
            WSHandler.on_send(obj, myStr)
            #print(row[1], ids)
            ids = []



def Do_rows(obj, z):
    print("Doing Rows")
    myStr = {}
    myStrA = {}
    myStrA['number'] = z
    if z < len(myRows):
        row = myRows[z]
        for i, val in enumerate(row):
            myStr[headers[i]] = val

        myStrA['frame'] = myStr
        myStr = json.dumps(myStrA)
        print("MY STR:", myStr)
        WSHandler.on_send(obj, myStr)

 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(5000, address='0.0.0.0')
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
