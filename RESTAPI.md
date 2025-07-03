RSETAPI.py restful接口功能
连接/断开PLC：/PLC/Control/ConnectPLC, /PLC/Control/DisconnectPLC
控制动作：
升降机：/PLC/Control/LifterUp, /PLC/Control/LifterDown
X/Y夹爪：/PLC/Control/ClampX_In, /PLC/Control/ClampX_Out, /PLC/Control/ClampY_In, /PLC/Control/ClampY_Out
电源：/PLC/Control/PowerIn, /PLC/Control/PowerOut
通信：/PLC/Control/CommIn, /PLC/Control/CommOut
复位：/PLC/Control/ResetIn, /PLC/Control/ResetOut
车道选择：/PLC/Control/LANE_SELECT_In, /PLC/Control/LANE_SELECT_Out
托盘插入/拔出：/PLC/Control/CRADLE_INSERT, /PLC/Control/CRADLE_EXTRACT
状态获取（通过 /get_control，支持 cradle、destaco、reset、lane_select）
固件版本获取：/get_version
通用控制接口：/set_control（支持 cradle、reset、lane_select）