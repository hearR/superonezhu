UART设备2
=========

UART简介2
---------

UART（Universal Asynchronous Receiver/Transmitter）通用异步收发传输器，UART 作为异步串口通信协议的一种，工作原理是将传输数据的每个字符一位接一位地传输。是在应用程序开发过程中使用频率最高的数据总线。

UART 串口的特点是将数据一位一位地顺序传送，只要 2 根传输线就可以实现双向通信，一根线发送数据的同时用另一根线接收数据。UART 串口通信有几个重要的参数，分别是波特率、起始位、数据位、停止位和奇偶检验位，对于两个使用 UART 串口通信的端口，这些参数必须匹配，否则通信将无法正常完成。UART 串口传输的数据格式如下图所示：

[示例图片]

- 起始位：表示数据传输的开始，电平逻辑为 “0” 。
- 数据位：可能值有 5、6、7、8、9，表示传输这几个 bit 位数据。一般取值为 8，因为一个 ASCII 字符值为 8 位。
- 奇偶校验位：用于接收方对接收到的数据进行校验，校验 “1” 的位数为偶数(偶校验)或奇数(奇校验)，以此来校验数据传送的正确性，使用时不需要此位也可以。
- 停止位： 表示一帧数据的结束。电平逻辑为 “1”。
- 波特率：串口通信时的速率，它用单位时间内传输的二进制代码的有效位(bit)数来表示，其单位为每秒比特数 bit/s(bps)。常见的波特率值有 4800、9600、14400、38400、115200等，数值越大数据传输的越快，波特率为 115200 表示每秒钟传输 115200 位数据。

访问串口设备
------------

应用程序通过 ``QuecOS`` 提供的 I/O 设备管理接口来访问串口硬件，相关接口如下所示：

+----------------------------------+----------------------------------+
| 函数                             | 描述                             |
+==================================+==================================+
| qosa_uart_open                   | 打开 UART 设备                   |
+----------------------------------+----------------------------------+
| qosa_uart_close                  | 关闭 UART 设备                   |
+----------------------------------+----------------------------------+
| qosa_uart_ioctl                  | 注册 uart 事件处理               |
+----------------------------------+----------------------------------+
| qosa_uart_read                   | UART读操作                       |
+----------------------------------+----------------------------------+
| qosa_uart_write                  | UART写操作                       |
+----------------------------------+----------------------------------+
| qosa_uart_read_available         | 获取UART读缓存剩余空间大小       |
+----------------------------------+----------------------------------+
| qosa_uart_write_available        | 获取UART写缓存剩余空间大小       |
+----------------------------------+----------------------------------+
| qosa_uart_register_cb            | 注册 UART 事件处理回调函数       |
+----------------------------------+----------------------------------+
| qosa_uart_check_support_baudrate | 检查 UART 是否支持某个波特率     |
+----------------------------------+----------------------------------+


打开 UART 设备
^^^^^^^^^^^^^^

通过配置需要打开的UART通道，调用此函数打开UART设备。

.. code-block:: c

   qosa_uart_error_e qosa_uart_open(qosa_uart_port_number_e port);

**参数描述：**


* ``qosa_uart_port_number_e`` - 串口设备号

**返回值描述：**
函数执行成功返回 QOSA_UART_SUCCESS ，否则返回其他\ ``qosa_uart_error_e``\ 枚举类型的类型的枚举值。

TODO：这里需要根据不同模块的情况介绍实际型号支持的真实情况，比如ASR UART0是做什么功能的，YX的UART0是做什么功能的

对于串口设备号\ ``qosa_uart_port_number_e``\ ，当前 QuecOS 目前支持以下几种串口的打开，对应 UART0 通常为主串口，UART1 通常为第二串口，UART2 通常为第三串口。对应的 USB AT 口对应 USB 驱动枚举的AT口，USB Modem 口对应 USB 驱动枚举的 Modem 口，USB NMEA 端口对应 USB 驱动枚举的NMEA端口通常为 GNSS 输出 NMEA 数据口。其对应的枚举原型如下：

.. code-block:: c

   /**
    * @enum  qosa_uart_port_number_e
    * @brief uart port number definition.
    */
   typedef enum
   {
       QOSA_PORT_NONE = -1,
       QOSA_UART_PORT_0,    /*!< uart0 */
       QOSA_UART_PORT_1,    /*!< uart1 */
       QOSA_UART_PORT_2,    /*!< uart2 */
       QOSA_UART_PORT_3,    /*!< uart3 */
       QOSA_USB_PORT_AT,    /*!< usb at port */
       QOSA_USB_PORT_MODEM, /*!< usb modem port */
       QOSA_USB_PORT_NMEA,  /*!< usb nmea port */
       QOSA_USB_PORT_ACM0,  /*!< usb acm0 port */
       QOSA_PORT_MAX,
   } qosa_uart_port_number_e;

对应\ ``qosa_uart_error_e`` 错误返回值有以下几种情况，参考如下枚举定义：

.. code-block:: c

   /**
    * @enum  qosa_uart_error_e
    * @brief uart error code definition.
    */
   typedef enum
   {
       QOSA_UART_SUCCESS = 0,
       QOSA_UART_EXECUTE_ERR = 1 | QOSA_UART_ERRCODE_BASE, /*!< 串口执行错误 */
       QOSA_UART_MEM_ADDR_NULL_ERR,                        /*!< 内存地址为空 */
       QOSA_UART_INVALID_PARAM_ERR,                        /*!< 无效参数 */
       QOSA_UART_OPEN_REPEAT_ERR,                          /*!< 串口重复打开 */
       QOSA_UART_NOT_OPEN_ERR,                             /*!< 串口未打开 */
   } qosa_uart_error_e;

注册 uart 事件处理
^^^^^^^^^^^^^^^^^^

通过控制接口，应用程序可以对串口设备进行配置，如设置串口属性、获取串口属性、获取RI/DTR/RTS/CTS/DCD状态、更改波特率、设置DTR回调函数等控制。控制函数如下所示：

.. code-block:: c

   qosa_uart_error_e qosa_uart_ioctl(qosa_uart_port_number_e port, qosa_uart_ioctl_cmd_e cmd, void *arg);

**参数描述：**


* ``qosa_uart_port_number_e`` - 串口设备号
* ``qosa_uart_ioctl_cmd_e`` - 控制命令
* ``void *arg`` - 控制命令参数

**返回值描述：**
函数执行成功返回 QOSA_UART_SUCCESS ，否则返回其他\ ``qosa_uart_error_e``\ 枚举类型的类型的枚举值。

对于\ ``qosa_uart_ioctl_cmd_e``\ 支持的 cmd 类型有如下定义：

.. code-block:: c

   /**
    * @enum  qosa_uart_ioctl_cmd_e
    * @brief uart ioctl cmd definition.
    */
   typedef enum
   {
       QOSA_UART_IOCTL_NONE,
       QOSA_UART_IOCTL_SET_DCB_CFG,     /*!< 设置串口属性 */
       QOSA_UART_IOCTL_GET_DCB_CFG,     /*!< 获取串口属性 */
       QOSA_UART_IOCTL_SET_CCIO_MODE,   /*!< 设置CCIO模式(仅EIGEN平台Uart可用) */
       QOSA_UART_IOCTL_RI_GET,          /*!< 获取RI状态 */
       QOSA_UART_IOCTL_RI_SET,          /*!< 设置RI状态 */
       QOSA_UART_IOCTL_DTR_GET,         /*!< 获取DTR状态 */
       QOSA_UART_IOCTL_RTS_SET,         /*!< 设置RTS状态 */
       QOSA_UART_IOCTL_RTS_GET,         /*!< 获取RTS状态 */
       QOSA_UART_IOCTL_CTS_GET,         /*!< 获取CTS状态 */
       QOSA_UART_IOCTL_DCD_GET,         /*!< 获取DCD状态 */
       QOSA_UART_IOCTL_DCD_SET,         /*!< 设置DCD状态 */
       QOSA_UART_IOCTL_CHANGE_BAUDRATE, /*!< 更改波特率 */
       QOSA_UART_IOCTL_RECORD_DTR_FUNC, /*!< 设置DTR回调函数 */
   } qosa_uart_ioctl_cmd_e;

其中对应 ``qosa_uart_ioctl_cmd_e``\ 具体枚举对应\ ``void *arg``\ 的类型参数类型如下表：

.. list-table::
   :header-rows: 1

   * - cmd类型
     - argv参数类型
   * - QOSA_UART_IOCTL_SET_DCB_CFG
     - qosa_uart_config_t
   * - QOSA_UART_IOCTL_GET_DCB_CFG
     - qosa_uart_config_t
   * - QOSA_UART_IOCTL_SET_CCIO_MODE
     - qosa_uart_mode_e


在 ``qosa_uart_config_t``\ 结构体中有 ``baud``\ 、\ ``data_bits``\ 、\ ``stop_bits``\ 、\ ``parity``\ 等参数，其中 ``qosa_uart_baud_e`` 在不同平台所支持能力不同，具体参数含义如下：

.. code-block:: c

   /**
    * @enum  qosa_uart_baud_e
    * @brief uart baud definition.
    */
   typedef enum
   {
       QOSA_UART_BAUD_AUTO = 0, /*!< Automatically detect baud rate */
       QOSA_UART_BAUD_1200 = 1200,
       QOSA_UART_BAUD_2400 = 2400,
       QOSA_UART_BAUD_4800 = 4800,
       QOSA_UART_BAUD_9600 = 9600,
       QOSA_UART_BAUD_10400 = 10400,
       QOSA_UART_BAUD_14400 = 14400,
       QOSA_UART_BAUD_19200 = 19200,
       QOSA_UART_BAUD_28800 = 28800,
       QOSA_UART_BAUD_33600 = 33600,
       QOSA_UART_BAUD_38400 = 38400,
       QOSA_UART_BAUD_57600 = 57600,
       QOSA_UART_BAUD_115200 = 115200,
       QOSA_UART_BAUD_187500 = 187500,
       QOSA_UART_BAUD_230400 = 230400,
       QOSA_UART_BAUD_460800 = 460800,
       QOSA_UART_BAUD_921600 = 921600,
       QOSA_UART_BAUD_1000000 = 1000000,
       QOSA_UART_BAUD_1843200 = 1843200,
       QOSA_UART_BAUD_2000000 = 2000000,
       QOSA_UART_BAUD_2100000 = 2100000,
       QOSA_UART_BAUD_3686400 = 3686400,
       QOSA_UART_BAUD_4000000 = 4000000,
       QOSA_UART_BAUD_4468750 = 4468750
   } qosa_uart_baud_e;

   /**
    * @enum  qosa_uart_databit_e
    * @brief uart databit definition.
    */
   typedef enum
   {
       QOSA_UART_DATABIT_7 = 7,
       QOSA_UART_DATABIT_8 = 8,
   } qosa_uart_databit_e;

   /**
    * @enum  qosa_uart_stopbit_e
    * @brief uart stopbit definition.
    */
   typedef enum
   {
       QOSA_UART_STOP_1 = 1,
       QOSA_UART_STOP_2 = 2,
   } qosa_uart_stopbit_e;

   /**
    * @enum  qosa_uart_paritybit_e
    * @brief uart paritybit definition.
    */
   typedef enum
   {
       QOSA_UART_PARITY_NONE, /*!< 无校验 */
       QOSA_UART_PARITY_ODD,  /*!< 奇校验 */
       QOSA_UART_PARITY_EVEN, /*!< 偶校验 */
   } qosa_uart_paritybit_e;

   /**
    * @enum  qosa_uart_flowctrl_e
    * @brief uart flowctrl definition.
    */
   typedef enum
   {
       QOSA_FC_NONE = 0, /*!< no flow control */
       QOSA_FC_HW,       /*!< hardware flow control */
       QOSA_FC_HW_RTS,   /*!< hardware flow control, RTS */
       QOSA_FC_HW_CTS,   /*!< hardware flow control, CTS */
   } qosa_uart_flowctrl_e;

   /**
    * @struct  qosa_uart_config_t
    * @brief uart config definition.
    */
   typedef struct
   {
       qosa_uart_baud_e      baudrate;   /*!< 波特率 */
       qosa_uart_databit_e   data_bit;   /*!< 数据位 */
       qosa_uart_stopbit_e   stop_bit;   /*!< 停止位 */
       qosa_uart_paritybit_e parity_bit; /*!< 校验位 */
       qosa_uart_flowctrl_e  flow_ctrl;  /*!< 流控 */
   } qosa_uart_config_t;

TODO: 针对于 ``qosa_uart_baud_e`` 在这里针对于平台提供不同平台的波特率支持情况

串口设备使用示例
----------------

UART示例程序展示了基于QuecOS系统的串口通信功能，主要实现了五种测试模式：周期发送数据、中断接收回显、主动轮询接收、波特率自动切换和AT模式切换。程序通过\ ``quec_uart_ind``\ 回调函数处理接收中断事件，当串口接收到数据时会自动触发回调，读取当前缓冲区数据并回传，同时支持通过\ ``g_uart_test_case``\ 全局变量动态切换工作模式。初始化时配置了115200波特率、8N1参数，并开启循环回调机制。示例不依赖特定硬件平台，通过修改\ ``QUEC_TEST_UART_PORT``\ 宏定义即可适配不同BSP的串口设备，适用于串口通信功能验证和模组测试场景。

TODO：下面代码示例中的注释太少了，需要补充

.. code-block:: c

   #include "qosa_sys.h"
   #include "qosa_uart.h"
   #include "qosa_def.h"
   #include "qosa_log.h"

   #include "uart_examples.h"

   /*===========================================================================
    *  Macro Definition
    ===========================================================================*/

   #define quec_demo_log(...) QOSA_LOG_D(LOG_TAG, ##__VA_ARGS__)

   /*===========================================================================
    *  Variate
    ===========================================================================*/

   static qosa_task_t  g_quec_uart_demo_task = QOSA_NULL;
   static qosa_uint8_t g_uart_data[1024] = {0};

   static qosa_uint16_t g_uart_test_case = QOSA_UART_DEMO_OUTPUT;

   /*===========================================================================
    *  Static API Functions
    ===========================================================================*/

   static void quec_uart_ind(qosa_uart_event_e ind_type, qosa_uart_port_number_e port, void *user_data)
   {
       switch (g_uart_test_case)
       {
           case QOSA_UART_DEMO_READ_1: {
               quec_demo_log("ind_type %d", ind_type);
               int read_length = qosa_uart_read_available(QUEC_TEST_UART_PORT);
               qosa_uart_read(QUEC_TEST_UART_PORT, (unsigned char *)&g_uart_data, read_length);

               quec_demo_log("recv uart data %s", g_uart_data);
               qosa_uart_write(QUEC_TEST_UART_PORT, (unsigned char *)g_uart_data, read_length);
           }
           break;
           default:
               break;
       }
   }

   static void quec_uart_demo_process(void *ctx)
   {
       int ret = 0;

       qosa_uart_status_monitor_t monitor = {0};
       monitor.callback = quec_uart_ind; /* 注册回调函数 */
       monitor.circ_en = 1;              /* 开启回调函数循环触发 */

       qosa_uart_register_cb(QUEC_TEST_UART_PORT, &monitor);

       qosa_uart_config_t dcb_config = {0};
       dcb_config.baudrate = QOSA_UART_BAUD_115200;
       dcb_config.data_bit = QOSA_UART_DATABIT_8;
       dcb_config.flow_ctrl = QOSA_FC_NONE;
       dcb_config.parity_bit = QOSA_UART_PARITY_NONE;
       dcb_config.stop_bit = QOSA_UART_STOP_1;

       qosa_uart_ioctl(QUEC_TEST_UART_PORT, QOSA_UART_IOCTL_SET_DCB_CFG, (void *)&dcb_config);

       qosa_uart_open(QUEC_TEST_UART_PORT);

       while (1)
       {
           switch (g_uart_test_case)
           {
               case QOSA_UART_DEMO_OUTPUT: {
                   qosa_task_sleep_sec(1);
                   qosa_uart_write(QUEC_TEST_UART_PORT, (unsigned char *)"hello Quectel\r\n", 15);
               }
               break;
               case QOSA_UART_DEMO_READ_1: {
                   qosa_task_sleep_sec(1);
                   /* Received data in uart callback */
               }
               break;
               case QOSA_UART_DEMO_READ_2: {
                   qosa_task_sleep_sec(5);
                   qosa_uart_read(QUEC_TEST_UART_PORT, (unsigned char *)&g_uart_data, 1024);

                   quec_demo_log("recv uart data %s", g_uart_data);
                   ret = qosa_uart_write(QUEC_TEST_UART_PORT, (unsigned char *)&g_uart_data, 1024);
                   quec_demo_log("qosa_uart_write ret = %d", ret);
               }
               break;
               case QOSA_UART_DEMO_BAUDRATE: {
                   const qosa_uint32_t baudRateList[] = {0, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600};

                   int i;
                   for (i = 0; i < sizeof(baudRateList) / sizeof(baudRateList[0]); i++)
                   {
                       qosa_uart_ioctl(QUEC_TEST_UART_PORT, QOSA_UART_IOCTL_CHANGE_BAUDRATE, (void *)&baudRateList[i]);
                       qosa_task_sleep_sec(1);
                       qosa_uart_write(QUEC_TEST_UART_PORT, (unsigned char *)"Baudrate TEST\r\n", 15);
                       qosa_task_sleep_sec(1);
                   }
               }
               break;
               case QOSA_UART_DEMO_CHANGE_CCIO_MODE: {
                   qosa_uart_mode_e ccio_mode;
                   int              i;
                   ccio_mode = QOSA_UART_MODE_NORMAL;
                   qosa_uart_ioctl(QUEC_TEST_UART_PORT, QOSA_UART_IOCTL_SET_CCIO_MODE, (void *)&ccio_mode);
                   qosa_uart_write(QUEC_TEST_UART_PORT, (unsigned char *)"Enter Uart Mode\r\n", 17);
                   for (i = 0; i < 20; i++)
                   {
                       qosa_uart_write(QUEC_TEST_UART_PORT, (unsigned char *)"Waiting...\r\n", 12);
                       qosa_task_sleep_sec(1);
                   }

                   ccio_mode = QOSA_UART_MODE_AT;
                   qosa_uart_write(QUEC_TEST_UART_PORT, (unsigned char *)"Enter AT Mode\r\n", 15);
                   qosa_task_sleep_sec(1); /* 等待发送结束 */
                   qosa_uart_ioctl(QUEC_TEST_UART_PORT, QOSA_UART_IOCTL_SET_CCIO_MODE, (void *)&ccio_mode);
                   qosa_task_sleep_sec(20);
               }
               break;
               default:
                   break;
           }
       }
   }

   /*===========================================================================
    *  Public API Functions
    ===========================================================================*/

   void quec_demo_uart_case_switch(qosa_uart_demo_case_e caseNo)
   {
       g_uart_test_case = caseNo;
   }

   void quec_demo_uart_init()
   {
       quec_demo_log("enter Quectel UART DEMO !!!");
       if (g_quec_uart_demo_task == QOSA_NULL)
       {
           qosa_task_create(
               &g_quec_uart_demo_task,
               CONFIG_QUECOS_UART_DEMO_TASK_STACK_SIZE,
               QUEC_UART_DEMO_TASK_PRIO,
               "uart_demo",
               quec_uart_demo_process,
               QOSA_NULL,
               1
           );
       }
   }
