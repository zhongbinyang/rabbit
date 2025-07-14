@echo on

curl -X POST --url http://192.168.137.175:5001/connect_plc
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"jtag\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"jtag\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"io\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"io\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"power\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"power\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"proximity_switch1\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"proximity_switch2\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x1_in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x1_out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x2_in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x2_out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y1_in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y1_out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y2_in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y2_out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"jtag_out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"jtag_in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"io_out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"io_in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"power_out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"power_in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"safety_light_grid\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x_out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x_in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y_out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y_in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.137.175:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"testing_ready\"}"
echo.
timeout /t 2 >nul


curl -X POST --url http://192.168.137.175:5001/disconnect_plc
echo.
timeout /t 2 >nul

pause