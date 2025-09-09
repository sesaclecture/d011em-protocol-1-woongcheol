#!/usr/bin/env python3
# pylint: disable=import-error

"""
GPIO 과제
- gpiozero 라이브러리 사용

UART 과제
- pyserial 라이브러리 사용
- UART 통신: 115200 bps, 8N1, 플로우 제어 없음
- TXD3/RXD3을 활용
"""

import sys
import time

from gpiozero import LED, Button
from serial import Serial


def blink_led() -> None:
    """
    [문제 1] 18번 핀에 연결된 LED를 1초 간격으로 ON/OFF를 10번 반복
    - gpiozero.LED 사용
    - 종료시 LED는 OFF 상태
    """
    
    led = LED(18)
    cnt = 0
    while cnt<10:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
        cnt += 1


def check_to_input_button() -> None:
    """
    [문제 2] 18번 핀 버튼 입력을 받아서
      - 눌렸을 때: 'pressed'
      - 뗐을 때:   'released'
    를 출력한다.
    - polling 방식으로 구현할 것.
    - 버튼 입력을 10번 받았으면 종료.
    """
    btn = Button(18, pull_up=True)
    prev = btn.is_pressed
    cnt = 0
    
    while cnt < 10:
        current = btn.is_pressed
        
        if current != prev:
            if current:
                cnt += 1
                print("pressed")
            else:
                print("released")
            prev = current

def blink_led_through_button() -> None:
    """
    [문제 3]
    - 12번: LED 출력
    - 13번: Button 입력
    - 버튼이 눌려 있는 동안에만 LED가 0.5초 간격으로 깜빡인다.
    - 버튼이 10번 눌려졌으면 종료.
    - 종료시 LED는 OFF 상태
    """
    # TODO: blink_led_through_button 구현

    btn = Button(13)
    led = LED(12)
    press_count = 0

    try:
        while press_count < 10:
            # 1. 버튼이 눌렸는지 확인
            if btn.is_pressed:
                # 2. 버튼이 눌리는 '순간'을 감지하여 카운트 증가
                press_count += 1
                print(f"Button pressed! Count: {press_count}")

                led.on()
                time.sleep(0.5)
                led.off()
                time.sleep(0.5)
                
            # 버튼이 눌리지 않았을 때는 잠시 대기하여 CPU 사용량을 줄임
            else:
                time.sleep(0.01)

    finally:
        # 5. 루프가 종료되면(10번 눌리면) 최종적으로 LED를 끔

        if led:
            led.off()  # LED를 끄고
            led.close() # LED가 사용하던 GPIO 핀 자원 해제
        if btn:
            btn.close() # Button이 사용하던 GPIO 핀 자원 해제
        print("Program finished. LED is off.")

def transmit_msg() -> None:
    """
    [문제 1] UART3로 "Hello World! {i}" 문자열을 1초마다 전송
    - 총 10번 전송 후 종료
    - 개행을 붙여 전송 (수신/테스트 편의)
    """
    # TODO: blink_led_through_button 구현

    ser = Serial("/dev/ttyAMA3", baudrate=115200, timeout=1.0)

    for i in range(10):
        msg = f"Hello World! {i}\n"
        ser.write(msg.encode())
        time.sleep(1)

def receive_msg() -> None:
    """
    [문제 2] UART3에서 줄 단위로 읽어 화면에 출력.
    - 'exit' (대소문자 무시) 라인을 수신하면 함수 종료
    """
    # ser = Serial("/dev/ttyAMA3", baudrate=115200, timeout=1.0)
    # msg = ""
    # temp_msg = ""

    # while True:
    #     temp_msg = ser.read().decode('utf-8')
    #     if temp_msg != "\n":
    #         msg += temp_msg
    #     elif msg != "exit":
    #         print(msg)
    #         msg = ""
    #     elif msg == "exit":
    #         print(msg)
    #         break

    ser = None
    try:
        ser = Serial("/dev/ttyAMA3", baudrate=115200, timeout=1.0)
        
        # 1. bytes를 모아둘 bytearray 버퍼 생성
        line_buffer = bytearray()

        while True:
            # 2. 한 바이트씩 읽기
            one_byte = ser.read()

            # 타임아웃으로 읽은 데이터가 없으면 계속 진행
            if not one_byte:
                continue
            
            # 3. 버퍼에 읽은 바이트 추가
            line_buffer.extend(one_byte)

            # 4. 읽은 바이트가 줄바꿈 문자(b'\n')이면 한 줄 처리 시작
            if one_byte == b'\n':
                # 5. 버퍼에 쌓인 bytes를 한번에 string으로 변환
                received_msg = line_buffer.decode('utf-8').strip()
                
                if received_msg:
                    print(received_msg)
                
                # 6. 소문자로 바꿔서 'exit'인지 확인 (대소문자 무시)
                if received_msg.lower() == 'exit':
                    break
                
                # 7. 다음 줄을 위해 버퍼 비우기
                line_buffer.clear()
    finally:
        # 8. 사용한 포트는 항상 닫아줌
        if ser:
            ser.close()

if __name__ == "__main__":
    # blink_led()
    # check_to_input_button()
    # blink_led_through_button()
    # transmit_msg()
    receive_msg()