import socket
import cv2
import numpy as np

def receive_udp_video():
    # 创建 UDP 套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定到指定地址和端口
    server_address = ('192.168.31.133', 4455)
    sock.bind(server_address)

    buffer = b''
    print('开始接收 UDP 视频数据...')
    try:
        while True:
            # 接收数据
            data, address = sock.recvfrom(4096)  # 一次最多接收 4096 字节
            buffer += data

            # 尝试解析视频帧
            try:
                # 这里假设可以直接用 OpenCV 解析 buffer 中的数据
                nparr = np.frombuffer(buffer, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow('UDP Video Stream', frame)
                    buffer = b''  # 清空缓冲区
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as e:
                pass
    except KeyboardInterrupt:
        print('停止接收数据')
    finally:
        # 关闭套接字和 OpenCV 窗口
        sock.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    receive_udp_video()