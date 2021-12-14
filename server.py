import paho.mqtt.client as mqtt
from busylight.lights.embrava import Blynclight
import logging

logging.basicConfig(level=logging.INFO)

class busylamp:
    lamp_color = (255, 255, 255)
    state = False

    def __init__(self):
        self.light = Blynclight.first_light()
        # self.light.blink((255, 255, 255), 1)

    def on(self):
        logging.debug('Turning lamp on')
        self.light.on(self.lamp_color)
        self.state = True

    def off(self):
        logging.debug('Turning lamp off')
        self.light.off()
        self.state = False

    def get_state(self):    
        logging.debug('Lamp status: '+ str(self.light.is_on))
        logging.debug(' status: '+ str(self.state))

        if (self.light.is_on):
            return "ON"
        else:
            return "OFF"

    def color(self, color):
        self.lamp_color = color
    
    def get_color(self):
        return self.lamp_color

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+str(rc))
    
    client.subscribe(root_topic + "/#")
    client.publish( root_topic + "/available/status","online", qos=0, retain=False)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.info(msg.topic+" "+str(msg.payload))
    
    payload = str(msg.payload.decode("UTF-8"))
    topic = msg.topic

    if root_topic + "/rgb/set" in topic:
        color_state_topic = root_topic + "/rgb/status"
        temp_color = payload.split(",")
        c = (int(temp_color[0]), int(temp_color[1]), int(temp_color[2]))
        lamp.color(c)
        color_status = ','.join([str(value) for value in lamp.get_color()])
        client.publish(color_state_topic,color_status)

    if root_topic + "/light/switch" in topic:
        state_topic = root_topic + "/light/status"
        if "ON" in payload:
            lamp.on()
        if "OFF" in payload:
            lamp.off()
        client.publish(state_topic,lamp.get_state())
            
def on_disconnect(client, userdata, rc):
   logging.info("client disconnected ok")    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

lamp = busylamp()

client.connect("192.168.200.8", 1883, 60)
root_topic = "busylamp"

client.loop_forever()
