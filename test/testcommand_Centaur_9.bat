@echo on

curl -X POST --url http://192.168.1.30:5001/connect_plc
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_holder\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_holder\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_fix\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_fix\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_opticalmodule\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_opticalmodule\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_debugmodule\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_debugmodule\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_mcio124module\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_mcio124module\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_rfmodule\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write_rfmodule\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write\", \"control_state\": \"load\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"write\", \"control_state\": \"unload\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_holder_work\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_holder_origin\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_fix_work\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_fix_origin\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_opticalmodule_work\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_opticalmodule_origin\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_debugmodule_work\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_debugmodule_origin\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_mcio124module_work\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_mcio124module_origin\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_rfmodule_work\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_rfmodule_origin\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_safedoor_front\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_safedoor_rear\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_safedoor_top\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"read_testerstatus\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/disconnect_plc
echo.
timeout /t 2 >nul

pause