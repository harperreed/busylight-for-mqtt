# busylight-for-mqtt
a quick python server for handling mqtt busy lights


Add to home assistant lights config:

```yaml
 - platform: mqtt
   object_id: busylamp
   name: "Busylamp"
   availability_topic: "busylamp/available/status"
   state_topic: "busylamp/light/status"
   command_topic: "busylamp/light/switch"
   rgb_state_topic: "busylamp/rgb/status"
   rgb_command_topic: "busylamp/rgb/set"
   effect_state_topic: "busylamp/effect/status"
   effect_command_topic: "busylamp/effect/set"
   effect_list:
    - "spectrum"
    - "gradient"
   qos: 0
   payload_on: "ON"
   payload_off: "OFF"
   optimistic: false
```