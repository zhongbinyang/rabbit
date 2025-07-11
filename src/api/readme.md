# PLC Control API Documentation

This API provides endpoints for PLC control, supporting both GET and POST requests. All endpoints return standard JSON responses.

> Default server port: `5001`

---

## Table of Contents

- [Connect to PLC](#connect-to-plc-connect_plc)
- [Disconnect PLC](#disconnect-plc-disconnect_plc)
- [Execute PLC Command](#execute-plc-command-execute_command)
- [Get API Version](#get-api-version-get_version)
- [Page Endpoints](#page-endpoints)

---

## Connect to PLC `/connect_plc`

- **Method**: GET / POST

- **Parameters**:
  
  - `Host` (string, optional, default: `192.168.1.11`)
  - `Port` (int, optional, default: `502`)

- **Response**:
  
  ```json
  {
  "Function": "ConnectPLC",
  "Result": true,
  "Message": "Connect PLC Successful 192.168.1.11:502",
  "timestamp": "2025-01-25 13:41:27_396084"
  }
  ```

- **Example**:
  
  ```
  curl "http://127.0.0.1:5001/connect_plc?Host=192.168.1.11&Port=502"
  ```

---

## Disconnect PLC `/disconnect_plc`

- **Method**: GET / POST

- **Parameters**: None

- **Response**:
  
  ```json
  {
  "Function": "DisconnectPLC",
  "Result": true,
  "Message": "Close Successful",
  "timestamp": "2025-01-25 13:43:47_847322"
  }
  ```

- **Example**:
  
  ```
  curl "http://127.0.0.1:5001/disconnect_plc"
  ```

---

## Execute PLC Command `/execute_command`

- **Method**: GET / POST

- **Parameters**:
  
  - `action` (string, required)

- **Response**:
  
  ```json
  {
  "Function": "execute_plc_command",
  "Result": true,
  "Message": "sample_action command successful",
  "timestamp": "2025-01-25 13:44:32_943210"
  }
  ```

- **Example**:
  
  ```
  curl -X POST "http://127.0.0.1:5001/execute_command" -H "Content-Type: application/json" -d '{"action": "sample_action"}'
  ```
  
  Note: The available action names can be found on the action configuration page.
  
  ![](/Users/zbyang/Library/Application%20Support/marktext/images/2025-07-11-15-20-28-image.png)

---

## Get API Version `/get_version`

- **Method**: GET / POST

- **Parameters**: None

- **Response**:
  
  ```json
  {
  "Function": "get_api_version",
  "Result": true,
  "Message": "1.0.0",
  "timestamp": "2025-01-25 13:50:00_000000"
  }
  ```

- **Example**:
  
  ```
  curl "http://127.0.0.1:5001/get_version"
  ```

---

## Page Endpoints

- `/io_setting`  — IO configuration page
- ![](/Users/zbyang/Library/Application%20Support/marktext/images/2025-07-11-15-22-04-image.png)
- `/action_setting` — Action configuration page
- 
- `/action_control` — Action control page
- ![](/Users/zbyang/Library/Application%20Support/marktext/images/2025-07-11-15-22-45-image.png)
- `/action_status` — Status monitoring page
- ![](/Users/zbyang/Library/Application%20Support/marktext/images/2025-07-11-15-23-06-image.png)
- `/` — API documentation page (supports `?format=json` for JSON format)
- ![](/Users/zbyang/Library/Application%20Support/marktext/images/2025-07-11-15-23-52-image.png)

---

## Error Response Examples

404:

```json
{
  "Function": "Error",
  "Result": false,
  "Message": "Resource not found",
  "timestamp": "..."
}
```

500:

```json
{
  "Function": "Error",
  "Result": false,
  "Message": "Internal server error",
  "timestamp": "..."
}
```

---

For further assistance, please contact the developer.
