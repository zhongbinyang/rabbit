curl "http://192.168.1.30:5001/connect_plc"

curl --request POST --url http://192.168.1.30:5001/execute_command --header 'content-type: application/json' --data '{ "action": "lifter_up" }'
curl --request POST --url http://192.168.1.30:5001/execute_command --header 'content-type: application/json' --data '{ "action": "lifter_down" }'


curl "http://192.168.1.30:5001/disconnect_plc"


curl --request POST \
  --url http://192.168.1.30:5001/execute_command \
  --header 'content-type: application/json' \
  --data '{
  "action": "Clamp_y2_out"
}'
