from datetime import datetime
import pytz

def test():
    test_list = [
        '1', '22', '333', '4444'
    ]
    print(datetime.datetime.now())  # 현재 날짜와 시간 출력
    for sss in test_list:
        yield sss  # 제너레이터로 각 요소 반환

def test1():
    print('test1')  # 'test1' 출력
    gen = test()    # 제너레이터 객체 생성
    print(datetime.datetime.now())  # 현재 날짜와 시간 출력
    return gen  # 제너레이터 객체 반환


def test2():
    # ISO 8601 날짜 문자열
    iso_date_str = '2024-07-26T08:18:46.797840Z'

    # 문자열을 datetime 객체로 변환
    datetime_obj = datetime.strptime(iso_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

    # 밀리초를 제거한 문자열 포맷으로 변환
    formatted_date_str = datetime_obj.strftime('%Y-%m-%dT%H:%M')

    print("원본 datetime 객체:", datetime_obj)
    print("밀리초 제거한 문자열:", formatted_date_str)


if __name__ == '__main__':
    test2()
    # gen = test1()  # test1() 함수 호출하여 제너레이터 객체 얻기
    # for item in gen:  # 제너레이터를 반복하여 각 요소 출력
    #     print(item)  # 각 요소를 출력
