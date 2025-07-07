# GET request example
curl -X GET "http://localhost:5001/execute_command?action=Test_Command"

# POST request example (form)
curl -X POST "http://localhost:5001/execute_command" \
  -d "action=Test_Command"

# POST request example (JSON)
curl -X POST "http://localhost:5001/execute_command" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "Test_Command"
  }'

# Minimal example with only required parameter
curl "http://localhost:5001/execute_command?action=Test_Command"

# Example to get JSON response
curl -X GET "http://localhost:5001/execute_command?action=Test_Command" \
  -H "Accept: application/json"