# rabbit

io_setting 命名原则
PLC：使用M或者D开头，比如 M10100。
Description: 有意义即可。clamp_x_in

action_setting 命名原则
Action Name: 小写字母，无空格，可以使用下划线连接，必须带有下划线，
    set操作的IO：下划线最后是动作：比如 clamp_x_in，clamp_x_out，power_on, power_off
    get操作的IO：下划线最后是state，比如 clamp_x2_home_state，
Description: 
    set操作的IO，使用PLC对应的数据即可：比如 M10100。
    get操作的IO，必须使用 on_off, up_down, inserted_extracted 等有意义的数据，会作为返回值返回。

    






