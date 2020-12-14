"""
串口数据收发
"""
import serial
# import serial.tools.list_ports
import time
import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)
class UsartData:
    """
    读取处理串口数据
    """
    def __init__(self, com, baud, timeout, logger=None):
        if logger is None:

            self.logger = logging
        else:
            self.logger = logger
        self.port = com
        self.baud = baud
        self.timeout = timeout
        self.logger.info('test log')
        try:
            # 打开串口，并得到串口对象
            self.uart = serial.Serial(self.port, self.baud, timeout=self.timeout)
            # 判断是否打开成功
            if not (self.uart.is_open):
                self.logger.error('无法打开串口')
        except Exception as e:
            self.logger.info({"串口连接异常：": e})

    # 打印设备基本信息
    def print_info(self):
        info_dict = {
            'name':self.uart.name,                # 设备名字
            'port':self.uart.port,                # 读或者写端口
            'baudrate':self.uart.baudrate,        # 波特率
            'bytesize':self.uart.bytesize,        # 字节大小
            'parity':self.uart.parity,            # 校验位
            'stopbits':self.uart.stopbits,         # 停止位
            'timeout':self.uart.timeout,# 读超时设置
            'writeTimeout':self.uart.writeTimeout,  # 写超时
            'xonxoff':self.uart.xonxoff,             # 软件流控
            'rtscts':self.uart.rtscts,           # 软件流控
            'dsrdtr':self.uart.dsrdtr,           # 硬件流控
            'interCharTimeout':self.uart.interCharTimeout,   # 字符间隔超时
        }
        self.logger.info(info_dict)
        return info_dict

    # 打开串口
    def open_serial(self):
        self.uart.open()

    # 关闭串口
    def close_Engine(self):
        self.uart.close()
        print(self.uart.is_open)  # 检验串口是否打开

    # 打印可用串口列表
    @staticmethod
    def Print_Used_Com():
        port_list = list(serial.tools.list_ports.comports())
        print(port_list)

    # 接收指定大小的数据
    # 从串口读size个字节。如果指定超时，则可能在超时后返回较少的字节；如果没有指定超时，则会一直等到收完指定的字节数。
    def read_Size(self, size):
        return self.uart.read(size=size)

    # 接收一行数据
    # 使用readline()时应该注意：打开串口时应该指定超时，否则如果串口没有收到新行，则会一直等待。
    # 如果没有超时，readline会报异常。
    def read_Line(self):
        data_read = self.uart.readline()
        # self.logger.info({'单片机读取数据':data_read})
        # 通过
        if str(data_read).count(',') > 2:

            # self.logger.info({'单片机读取数据处理后':str(data_read)[2:-5]})
            return str(data_read)[2:-5]
        else:
            return None

    # 发数据
    def send_data(self, data):
        self.uart.write(data.encode())

    # 更多示例
    # self.uart.write(chr(0x06).encode("utf-8"))  # 十六制发送一个数据
    # print(self.uart.read().hex())  #  # 十六进制的读取读一个字节
    # print(self.uart.read())#读一个字节
    # print(self.uart.read(10).decode("gbk"))#读十个字节
    # print(self.uart.readline().decode("gbk"))#读一行
    # print(self.uart.readlines())#读取多行，返回列表，必须匹配超时（timeout)使用
    # print(self.uart.in_waiting)#获取输入缓冲区的剩余字节数
    # print(self.uart.out_waiting)#获取输出缓冲区的字节数
    # print(self.uart.readall())#读取全部字符。

    # 接收数据
    # 一个整型数据占两个字节
    # 一个字符占一个字节

    def recive_data(self, way):
        # 循环接收数据，此为死循环，可用线程实现
        print("开始接收数据：")
        while True:
            try:
                # 一个字节一个字节的接收
                if self.uart.in_waiting:
                    if (way == 0):
                        for i in range(self.uart.in_waiting):
                            print("接收ascii数据：" + str(self.read_Size(1)))
                            data1 = self.read_Size(1).hex()  # 转为十六进制
                            data2 = int(data1, 16)  # 转为十进制print("收到数据十六进制："+data1+"  收到数据十进制："+str(data2))
                    if (way == 1):
                        # 整体接收
                        # data = self.main_engine.read(self.main_engine.in_waiting).decode("utf-8")#方式一
                        data = self.uart.read_all()  # 方式二print("接收ascii数据：", data)
            except Exception as e:
                print("异常报错：", e)

if __name__ == '__main__':
    # 示例
    usart_obj = UsartData('com8', 115200, timeout=1)
    usart_data = usart_obj.read_Line()
    logging.info({'usart_data':usart_data})
