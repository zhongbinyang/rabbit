@echo on

curl -X POST --url http://192.168.1.30:5001/connect_plc
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul


curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul



curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"lifter\", \"control_state\": \"up\"}"
echo.
timeout /t 2 >nul



curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"power\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"power\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp1\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp1\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp1_speediness\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp1_speediness\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp2_speediness\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp2_speediness\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp2\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp2\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp3\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp3\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp3_speediness\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp3_speediness\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp4\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp4\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp4_speediness\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp4_speediness\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp5\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp5\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp5_speediness\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp5_speediness\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp6\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp6\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp6_speediness\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp6_speediness\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp7\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp7\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp7_speediness\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp7_speediness\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp8\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp8\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp8_speediness\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp8_speediness\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp9\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp9\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp9_speediness\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"osfp9_speediness\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"eth_usb\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"eth_usb\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"fnm\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"fnm\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"eth_usb_led\", \"control_state\": \"in\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"manual_auto\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"start\", \"control_state\": \"on\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"stop\", \"control_state\": \"on\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"buzzer\", \"control_state\": \"enable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"buzzer\", \"control_state\": \"disable\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"test_ready\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"device_status\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"reset_flow\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"auto_flow\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"alarm\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"tray_in_1\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"tray_in_2\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x1_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x1_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x2_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x2_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y1_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y1_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y2_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y2_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"lifter_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"lifter_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"power_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"power_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_1_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_1_mediate_point\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_1_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_2_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_2_mediate_point\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_2_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_3_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_3_mediate_point\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_3_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_4_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_4_mediate_point\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_4_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_5_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_5_mediate_point\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_5_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_6_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_6_mediate_point\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_6_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_7_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_7_mediate_point\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_7_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_8_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_8_mediate_point\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_8_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_9_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_9_mediate_point\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"osfp_9_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"eth_usb_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"eth_usb_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"fnm_home\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/get_control -H "content-type: application/json" -d "{\"control_name\": \"fnm_in_place\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"lifter\", \"control_state\": \"down\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_x\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul

curl -X POST --url http://192.168.1.30:5001/set_control -H "content-type: application/json" -d "{\"control_name\": \"clamp_y\", \"control_state\": \"out\"}"
echo.
timeout /t 2 >nul



curl -X POST --url http://192.168.1.30:5001/disconnect_plc
echo.
timeout /t 2 >nul

pause