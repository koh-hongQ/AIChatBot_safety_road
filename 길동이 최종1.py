from openai import OpenAI
import os
import requests
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from tkinter import Toplevel
import time


# 전체화면 토글 함수
def toggle_fullscreen(event=None):
    is_fullscreen = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not is_fullscreen)

# 전체화면 종료 함수
def end_fullscreen(event=None):
    root.attributes("-fullscreen", False)


# Store your OpenAI API key in an environment variable or secure file
client = OpenAI(api_key="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")

# 보안등 API URL
SECURITY_LIGHTS_API_URL = "https://api.odcloud.kr/api/15128084/v1/uddi:6af7ce5f-4a0a-41ce-a0eb-fa3653c61737"
# 가로등 API URL
ROAD_LIGHTS_API_URL = "https://api.odcloud.kr/api/15012092/v1/uddi:aa711816-14bd-44c0-b5e4-e8a7ccc38ec0"


def count_matching_elements(data, substring):
    # 데이터를 필터링하여 "소재지도로명주소"에 주어진 문자열(substring)이 포함된 요소를 찾음
    matching_elements = [item for item in data['data'] if substring in item['소재지도로명주소']]
    
    # 매칭된 요소의 개수를 반환
    return len(matching_elements)

# 보안등 API 호출 함수
def get_security_lights_count(user_input):
    params = {
        "page": 1,
        "perPage": 10458,
        "search": user_input  # 주소를 검색 파라미터로 전달
    }

    headers = {
        "Authorization": "Infuser Wrd5rCy26XBJ9hLYKPOu6OAOVEfgl2EL9EPQ26DSotMHsRj8OqwDpkC3PsHMZay4Gc351TTjJrne7XZyjPXP3w=="
    }

    response = requests.get(SECURITY_LIGHTS_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        a = response.json()
        count = count_matching_elements(a, user_input)
        return count
    else:
        return "API 요청 실패"


# "1km 당 보행행등의 개수의 순위퍼센트" 데이터를 리스트로 저장
percentile_ranks2 = [
    93.35335631, 13.31534748, 89.05714583, 85.00629492, 88.06486698, 44.28194425, 12.6758041,
    15.16585675, 16.84291239, 82.76529244, 77.76492399, 33.20862925, 53.9081885, 28.11842869,
    42.07851421, 54.75481511, 91.79782025, 38.23322187, 38.13184168, 57.40644849, 32.84985087,
    30.61674873, 2.942648497, 84.17366896, 71.41986468, 60.86767247, 66.66917575, 97.21076418,
    56.7772011, 97.21076418, 8.331082228, 81.86855648, 95.72071176, 85.67664241, 31.93486951,
    97.21076418, 97.21076418, 11.54552638, 96.07607742, 54.79657108, 68.98617706, 97.21076418,
    97.21076418, 58.62163545, 77.19086707, 4.648027295, 0.171565025, 43.09337406, 97.21076418,
    50.30436918, 39.97616179, 97.21076418, 97.21076418, 12.46745549, 63.30968402
]


#보행등 관련 함수
def count_matching_elements2(data, substring):

    total = 0  # 합산할 변수 초기화

    for item in data['data']:
        # 주소에 substring이 포함되어 있는지 확인
        if substring in item.get('주소'):
            pedestrian_light = item.get("보행등")
            
            # '보행등' 값이 없거나 None이면 루프를 종료하고 '자료없음' 반환
            if pedestrian_light is None:
                return "자료없음"
                break
            
            # 값이 int 타입일 경우 합산
            if isinstance(pedestrian_light, int):
                total += pedestrian_light

    return total  # 루프가 끝나면 총합 반환

def get_rank_by_address2(data, substring, percentile_ranks3):
   
    for index, item in enumerate(data['data']):
        # "주소" 필드에서 주어진 substring 찾기
        if substring in item['주소']:
            # 매칭된 인덱스를 기준으로 순위 퍼센트 반환
            return percentile_ranks2[index]
    return None  # 매칭되는 항목이 없을 경우




# 보행등 API 호출 함수
def get_security_lights_count2(user_input):
    params = {
        "page": 1,
        "perPage": 55,
        "search": user_input  # 주소를 검색 파라미터로 전달
    }

    headers = {
        "Authorization": "Infuser Wrd5rCy26XBJ9hLYKPOu6OAOVEfgl2EL9EPQ26DSotMHsRj8OqwDpkC3PsHMZay4Gc351TTjJrne7XZyjPXP3w=="
    }

    response = requests.get(ROAD_LIGHTS_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        a = response.json()
        count2 = count_matching_elements2(a, user_input)
        return count2
    else:
        return "API 요청 실패"
# 보행등 순위 API 호출 함수
def get_security_lights_count2_1(user_input):
    params = {
        "page": 1,
        "perPage": 55,
        "search": user_input  # 주소를 검색 파라미터로 전달
    }

    headers = {
        "Authorization": "Infuser Wrd5rCy26XBJ9hLYKPOu6OAOVEfgl2EL9EPQ26DSotMHsRj8OqwDpkC3PsHMZay4Gc351TTjJrne7XZyjPXP3w=="
    }

    response = requests.get(ROAD_LIGHTS_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        a = response.json()
        count2_1 = get_rank_by_address2(a, user_input, percentile_ranks3)
        return count2_1
    else:
        return "API 요청 실패"





# "1km 당 차도등의 개수의 순위퍼센트" 데이터를 리스트로 저장
percentile_ranks3 = [
    90.68121253, 1.988645077, 87.62455884, 80.29114193, 79.91564815,
    54.83623867, 17.13527928, 21.27928053, 19.07828307, 76.8047172,
    77.35089005, 23.12424232, 58.89597522, 39.08550892, 51.18479838,
    59.77197944, 90.07042374, 20.29653505, 11.25890965, 46.91686267,
    42.87791142, 21.15086984, 0.209942706, 64.59771918, 63.45493155,
    22.27663183, 63.41926255, 23.00512079, 70.87264984, 64.52417275,
    30.07423316, 62.6231058, 92.44250473, 87.59494662, 35.47653809,
    95.2708108, 95.2708108, 15.19929243, 89.45724251, 71.84022611,
    73.28880038, 74.07501432, 74.46962346, 73.80918749, 83.12830954,
    30.13332179, 0.017340408, 34.71099991, 95.2708108, 48.67259512,
    42.02358646, 84.28640597, 68.29258918, 42.13847971, 76.17884451
]
#차도등 관련 함수
def count_matching_elements3(data, substring):
    total = 0  # 합산할 변수 초기화

    for item in data['data']:
        # 주소에 substring이 포함되어 있는지 확인
        if substring in item.get('주소'):
            pedestrian_light = item.get("차도등")
            
            # '보행등' 값이 없거나 None이면 루프를 종료하고 '자료없음' 반환
            if pedestrian_light is None:
                return "자료없음"
                break
            
            # 값이 int 타입일 경우 합산
            if isinstance(pedestrian_light, int):
                total += pedestrian_light

    return total  # 루프가 끝나면 총합 반환

def get_rank_by_address3(data, substring, percentile_ranks3):
   
    for index, item in enumerate(data['data']):
        # "주소" 필드에서 주어진 substring 찾기
        if substring in item['주소']:
            # 매칭된 인덱스를 기준으로 순위 퍼센트 반환
            return percentile_ranks3[index]
    return None  # 매칭되는 항목이 없을 경우

# 차도등 API 호출 함수
def get_security_lights_count3(user_input):
    params = {
        "page": 1,
        "perPage": 55,
        "search": user_input  # 주소를 검색 파라미터로 전달
    }

    headers = {
        "Authorization": "Infuser Wrd5rCy26XBJ9hLYKPOu6OAOVEfgl2EL9EPQ26DSotMHsRj8OqwDpkC3PsHMZay4Gc351TTjJrne7XZyjPXP3w=="
    }

    response = requests.get(ROAD_LIGHTS_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        a = response.json()
        count3 = count_matching_elements3(a, user_input)
        return count3
    else:
        return "API 요청 실패"
# 차도등 순위 API 호출 함수
def get_security_lights_count3_1(user_input):
    params = {
        "page": 1,
        "perPage": 55,
        "search": user_input  # 주소를 검색 파라미터로 전달
    }

    headers = {
        "Authorization": "Infuser Wrd5rCy26XBJ9hLYKPOu6OAOVEfgl2EL9EPQ26DSotMHsRj8OqwDpkC3PsHMZay4Gc351TTjJrne7XZyjPXP3w=="
    }

    response = requests.get(ROAD_LIGHTS_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        a = response.json()
        count3_1 = get_rank_by_address3(a, user_input, percentile_ranks3)
        return count3_1
    else:
        return "API 요청 실패"



# "안전등급" 데이터를 리스트로 저장
safety = ['위험', '매우 안전', '위험', '위험', '위험', '안전', '매우 안전', '매우 안전', '매우 안전', '위험', '위험', '안전', '보통', '안전', '안전', '보통', '위험', '매우 안전', '매우 안전', '보통', '안 전', '매우 안전', '매우 안전', '위험', '보통', '안전', '보통', 'nan', '보통', 'nan', '매우 안전', '보통', '위험', '위험', '안전', 'nan', 'nan', '매우 안전', '위험', '보통', '보통', 'nan', 'nan', '보통', '위 험', '매우 안전', '매우 안전', '안전', 'nan', '안전', '안전', 'nan', 'nan', '안전', '보통']
# 안전등급 함수    
def get_rank_by_address4(data, substring, safety):
   
    for index, item in enumerate(data['data']):
        # "주소" 필드에서 주어진 substring 찾기
        if substring in item['주소']:
            # 매칭된 인덱스를 기준으로 순위 퍼센트 반환
            return safety[index]
    return None  # 매칭되는 항목이 없을 경우
# 안전등급 API 호출 함수
def get_security_lights_count4(user_input):
    params = {
        "page": 1,
        "perPage": 55,
        "search": user_input  # 주소를 검색 파라미터로 전달
    }

    headers = {
        "Authorization": "Infuser Wrd5rCy26XBJ9hLYKPOu6OAOVEfgl2EL9EPQ26DSotMHsRj8OqwDpkC3PsHMZay4Gc351TTjJrne7XZyjPXP3w=="
    }

    response = requests.get(ROAD_LIGHTS_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        a = response.json()
        count4 = get_rank_by_address4(a, user_input, safety)
        return count4
    else:
        return "API 요청 실패"



# 챗봇 메인 코드
def create_chatbot_window():

    global root  # root를 전역으로 선언하여 다른 함수에서 접근 가능하도록 함
    root = tk.Tk()

    # Loading 팝업 띄우기
    loading_popup = Toplevel(root)
    loading_popup.title("Loading")
    loading_label = tk.Label(loading_popup, text="Loading...", font=("Times New Roman", 14))
    loading_label.pack(padx=20, pady=20)
    loading_popup.geometry("200x100")
    loading_popup.transient(root)
    loading_popup.grab_set()
    loading_popup.update()  # 팝업 업데이트

    # # 봇 응답 처리
    time.sleep(3)  # 여기서 실제 작업을 수행 (예: AI 응답 생성)

    

    root.title("길동이")


    # 전체 화면 모드 설정
    root.attributes("-fullscreen", True)
    root.bind("<F11>", toggle_fullscreen)  # F11 눌렀을 때 전체화면 토글
    root.bind("<Escape>", end_fullscreen)  # Escape 눌렀을 때 전체화면 종료

    # 창 배경 색을 아주 연한 핑크색으로 설정
    root.config(bg="#FFEBEE")  # 연한 핑크색 배경

    # 화면 상단에 전체화면 종료 버튼 추가
    end_fullscreen_button = tk.Button(root, text="Exit fullscreen", font=("Times New Roman", 13), bg="orchid", fg="white", command=end_fullscreen)
    end_fullscreen_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    # 메시지 출력창 (스크롤이 가능한 텍스트 위젯)
    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, bg="#FFFFFF", font=("Arial", 10), fg="#0000FF")  # 파란란색 텍스트
    chat_display.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
    
    # 배너 문구 삽입
    banner_label = tk.Label(root, text="Enter the Road Names of Departure and Destination", font=("Times New Roman", 20, "bold"))
    banner_label.grid(row=0, column=0, columnspan=2, pady=10)


    # 출발지 주소 라벨과 입력창 (위로 조금 이동)
    departure_label = tk.Label(root, text="Departure Point: ", font=("Times New Roman", 12), bg="#FFEBEE")  # 배경색 맞추기
    departure_label.grid(row=2, column=0, padx=20, pady=5, sticky="e")
    departure_input = tk.Entry(root, width=40, font=("Arial", 10))
    departure_input.grid(row=2, column=1, padx=20, pady=5, sticky="w")

    # 도착지 주소 라벨과 입력창 (위로 조금 이동)
    destination_label = tk.Label(root, text="Destination: ", font=("Times New Roman", 12), bg="#FFEBEE")  # 배경색 맞추기
    destination_label.grid(row=3, column=0, padx=20, pady=5, sticky="e")
    destination_input = tk.Entry(root, width=40, font=("Arial", 10))
    destination_input.grid(row=3, column=1, padx=20, pady=5, sticky="w")

    # 팝업 닫기
    loading_popup.destroy()


    # 메인 챗봇 코드
    def main():

        # 로딩 팝업 생성
        loading_popup = Toplevel(root)
        loading_popup.title("Loading")
        loading_label = tk.Label(loading_popup, text="Loading...Please wait for about 1 minute.", font=("Times New Roman", 14))
        loading_label.pack(padx=20, pady=20)
        loading_popup.geometry("800x100")
        loading_popup.transient(root)  # 부모 창과 관련된 팝업
        loading_popup.grab_set()  # 부모 창과의 상호작용 차단
        loading_popup.update()  # 팝업 업데이트

        # # 봇 응답 처리
        time.sleep(5)  # 여기서 실제 작업을 수행 (예: AI 응답 생성)


        loading_popup.destroy()
      
        messages = [
            {"role": "system", "content": 'you are a helpful assistant. 입력받은 user_input1에서 user_input2로 걸어서 가는데, 그 사이의 모든 안전한 *동대문구 안의 도로명 주소* 를 알려줘. 형식은 다른 문자열 붙이지 말고 "user_input1, 이문로, 석관로, 왕산로, 회기로, 안암로, user_input2, longitude of user_input1, latitude of user_input1, longitude of user_input2, latitude of user_input2" 예시처럼 순서대로. longitude of user_input1, latitude of user_input1, longitude of user_input2, latitude of user_input2 숫자로. 출력 문자열에 절대 따옴표가 있으면 안돼. '}
        ]

        user_input1 = departure_input.get()
        user_input2 = destination_input.get()
            
        if user_input1.lower() == '1' or user_input2.lower() == '1':  # 종료 조건
            root.quit()

        if user_input1.strip() != "" and user_input2.strip() != "":
            # 사용자 메시지 출력
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"Departure Point: {user_input1}\nDestination: {user_input2}\n\n")
            chat_display.config(state=tk.DISABLED)



            # 대화에 사용자 메시지 추가
            messages.append({"role": "user", "content": f"{user_input1} {user_input2}"})

            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-4o",  # 모델 이름 수정
                messages=messages
            )

            bot_response = response.choices[0].message.content



            # GPT가 생성한 도로명 주소, 경도,위도들을 리스트로 변환
            addresses = bot_response.split(',')  # 쉼표로 구분된 도로명 주소 처리

            # 마지막 4개의 자료를 pop해서 각 변수에 저장
            user_input2_y = addresses.pop()
            user_input2_x = addresses.pop()
            user_input1_y = addresses.pop()
            user_input1_x = addresses.pop()

            
            bot_response += f"""\n\n
                "길동이..계산 중.. 출발지의 도로명 주소를 바탕으로 경도, 위도를 계산 중... "
                "출발지({user_input1})의 경도: {user_input1_x}"
                "출발지({user_input1})의 위도: {user_input1_y}"
                "길동이..계산 중.. 도착지의 도로명 주소를 바탕으로 경도, 위도를 계산 중... "
                "도착지({user_input2})의 경도: {user_input2_x}"
                "도착지({user_input2})의 위도: {user_input2_y}"\n\n
                "길동이: 계산한 좌표를 바탕으로 '서울특별시 동대문구 지도'에 '출발지와 도착지의 최단경로'를 빨간 선으로 표시했습니다! 팝업된 '서울특별시 동대문구 지도'를 확인해주세요."\n
                "길동이: 팝업된 지도를 전체화면으로 만들고, 돋보기 버튼을 누르시면 최단경로를 확대해서 자세히 볼 수 있습니다!"
                \n\n
                "길동이...안전 경로...계산 중..."
                \n
                \n
                \n
                \n
                "길동이: 제가 추천하는 안전한 경로는 이렇습니다. \n{addresses} 순서!"
                \n
                \n
                \n
                \n
                "길동이: 이제 각 경로의 주소마다 안전 등급을 확인하겠습니다. 안전 등급은 '매우 안전, 안전, 보통, 위험' 4단계로 나뉩니다. 어두운 저녁에도 해당 주소의 거리가 밝아야 범죄율이 줄어든다는 근거에 따라, '1km 당 보안등 혹은 가로등 개수가 많을 수록' 안전하다고 판단했고 또한 안전 등급이 높게 선정했습니다."  
                \n
                "길동이: 동대문구 보안등과 가로등 데이터 API를 불러오겠습니다." 
                \n\n
                "길동이...안전 등급... 계산 중...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n "

                 """


            # 각 도로명 주소에 대해 함수 호출 및 출력
            for address in addresses:
                address = address.strip()  # 공백 제거
                
                # 각 함수 호출
                count = get_security_lights_count(address)
                count2 = get_security_lights_count2(address)
                count2_1 = get_security_lights_count2_1(address)
                count3 = get_security_lights_count3(address)
                count3_1 = get_security_lights_count3_1(address)
                count4 = get_security_lights_count4(address)
                
                # 결과 포맷을 bot_response에 추가
                bot_response += f"""
                "{address}의 보안등 개수: {count}"
                "{address}의 가로등(보행등) 개수: {count2}"
                "{address}의 가로등(보행등) 개수는 동대문구 안에서 상위 {count2_1}% 입니다."
                "{address}의 가로등(차도등) 개수: {count3}"
                "{address}의 가로등(차도등) 개수는 동대문구 안에서 상위 {count3_1}% 입니다."
                "***{address}의 안전 등급은 '{count4}' 입니다.***"
                """


            bot_response += f"""\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
                 """







            # 대화 맥락에 봇의 응답 추가
            messages.append({"role": "assistant", "content": bot_response})

            # 이미지 로드 및 설정
            image = Image.open("길동이.png")  # 이미지 경로를 변경하세요
            image = image.resize((30, 30))  # 적절한 크기로 조정
            photo = ImageTk.PhotoImage(image)
            # 이미지 삽입
            chat_display.image_create(tk.END, image=photo)
           
            # 봇 응답 출력
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"길동이...계산 중... {bot_response}\n")
            chat_display.config(state=tk.DISABLED)

            # 이미지 로드 및 설정
            image2 = Image.open("길동이.png")  # 이미지 경로를 변경하세요
            image2 = image2.resize((30, 30))  # 적절한 크기로 조정
            photo2 = ImageTk.PhotoImage(image2)
            # 이미지 삽입
            chat_display.image_create(tk.END, image=photo2)
           
            # 봇 응답 출력
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"""
                "길동이: 안전 경로마다 안전 등급은 잘 보셨나요? 최단경로 지도를 참고해서 목적지까지 빠르게 가는것도 좋지만, "\n
                "길동이: 안전 등급이 '위험','보통'인 길은 주의하시길 바래요. 지도에서 최단경로 근처의 다른 길로 우회해서 가는 것도 하나의 방법입니다! "\n
                "길동이: 오늘도 안전한 귀갓길 되시길! 길동이는 여러분의 안전과 늘 함께해요 ~ "

                \n
                \n

                "길동이: 새로운 경로에 대해 또 궁금하시면, 먼저 팝업된 지도 창을 닫고, 출발지와 도착지의 도로명 주소를 다시 입력한 후 'Send' 버튼을 눌러주세요!  "
                 """
            )
            chat_display.config(state=tk.DISABLED)

            
            
            
            
            
            #동대문구 지도
            G = ox.graph_from_place('동대문구, 서울, 대한민국', network_type="drive", truncate_by_edge=True)

            # 원점과 목적지 노드 찾기
            orig_node = ox.nearest_nodes(G, float(user_input1_x), float(user_input1_y))  # 출발지 (경도, 위도)
            dest_node = ox.nearest_nodes(G, float(user_input2_x), float(user_input2_y))   # 도착치 (경도, 위도)

            # 최단 경로 계산
            route = nx.shortest_path(G, orig_node, dest_node, weight='length')

            # 작업이 끝나면 로딩 팝업을 닫음
            fig, ax = ox.plot_graph_route(G, route, node_size=0)



            # 입력창 초기화
            departure_input.delete(0, tk.END)
            destination_input.delete(0, tk.END)

            # 화면 스크롤 맨 아래로
            chat_display.yview(tk.END)
            
            
            
    
    
    # 보내기 버튼
    send_button = tk.Button(root, text="Send", width=10, font=("Times New Roman", 12), bg="#90EE90", fg="black", command=main)
    send_button.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    # 레이아웃 확장
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)

    # 창 실행
    root.mainloop()
        
# 챗봇 실행
create_chatbot_window()