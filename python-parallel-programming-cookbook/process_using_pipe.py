import multiprocessing as mp

def create_items(pipe):
    output_pipe, _ = pipe
    for item in range(10):
        output_pipe.send(item)
    output_pipe.close()

def multiply_items(pipe_1, pipe_2):
    close, input_pipe = pipe_1
    close.close()
    output_pipe, _ = pipe_2
    try:
        while True:
            item = input_pipe.recv()
            output_pipe.send(item * item)
    except EOFError:
        output_pipe.close()

if __name__ == '__main__':
    # 第一进程管道发出数据
    pipe_1 = mp.Pipe(True)
    process_pipe_1 = mp.Process(target=create_items, args=(pipe_1,))
    process_pipe_1.start()
    # 第二个进程管道接收数据并计算
    pipe_2 = mp.Pipe(True)
    process_pipe_2 = mp.Process(target=multiply_items, args=(pipe_1,pipe_2,))
    process_pipe_2.start()
    pipe_1[0].close()
    pipe_2[0].close()
    try:
        while True:
            print(pipe_2[1].recv())
    except EOFError:
        print("End of program")