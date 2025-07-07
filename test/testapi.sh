# GET request example
curl -X GET "http://localhost:5001/PLC/Control/execute_command?command_addr=1000&parameters=1&status_addr=2000&expected_value=1&action_name=Test_Command"

# POST request example
curl -X POST "http://localhost:5001/PLC/Control/execute_command" \
  -d "command_addr=1000&parameters=1&status_addr=2000&expected_value=1&action_name=Test_Command"

  curl -X POST "http://localhost:5001/PLC/Control/execute_command" \
  -H "Content-Type: application/json" \
  -d '{
    "command_addr": "1000",
    "parameters": "1",
    "status_addr": "2000",
    "expected_value": "1",
    "action_name": "Test_Command"
  }'

# Minimal example with only required parameter
curl "http://localhost:5001/PLC/Control/execute_command?command_addr=1000"

# Example to get JSON response
curl -X GET "http://localhost:5001/PLC/Control/execute_command?command_addr=1000" \
  -H "Accept: application/json"