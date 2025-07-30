'''
在 Python 中，struct 模块可以用于将数据打包成二进制格式或从二进制格式解包。
主要实现逻辑是完成 Python 数值和C语言结构体的转换。这里涉及到格式符的概念。

格式符用于指定数据的类型和字节顺序。
! 表示网络字节顺序（大端）big-endian
Q 表示无符号长长整数，对应 C 语言 unsigned long long 类型，Python 中对应 int 类型
d 表示双精度浮点数，对应 C 语言 double 类型，Python 中对应 float 类型
'''
import struct

def float_to_binary(num):
    bits = struct.unpack('!Q', struct.pack('!d', num))[0]
    return bin(bits)[2:].zfill(64)

# 示例：3.5 的二进制表示
binary = float_to_binary(3.5)
print(f'3.5 的二进制表示为: {binary}')
print(f'符号位: {binary[0]}')
print(f'指数位: {binary[1:12]}')
print(f'尾数位: {binary[12:]}')