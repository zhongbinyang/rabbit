curl --request POST \
  --url http://127.0.0.1:5001/execute_command \
  --header 'content-type: application/json' \
  --data '{
  "action": "lifter_up"
}'