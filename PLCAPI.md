PLCAPI.py 的 PLC 类主要功能
连接/断开PLC：connectPLC, disconnectPLC
控制动作：
升降机：lifterUp, lifterDown
X/Y夹爪：clampX_in, clampX_out, clampY_in, clampY_out
电源：powerIn, powerOut
通信：commIn, commOut
复位：reset_on, reset_off
车道选择：lane_select_on, lane_select_off
托盘插入/拔出：cradle_inserted, cradle_extracted
状态获取：
托盘状态：get_cradle_state
destaco状态：get_destaco_state
复位状态：get_reset_state
车道选择状态：get_lane_select_state
PLC固件版本：get_plc_firmware