from utils import EasySSH
from random import randint as rand


__version__ = (1, 0, 0)
__version_str__ = '.'.join(map(str, __version__))


__info__ = \
''' $ EasySSH 란?
    : EasySSH는 원격지 서버의 ssh 연결을 보다 쉽게 다루기 위해 만든 유틸리티다.
    : 더 나아가, 원격지 서버에서 파이썬을 실행하여 로컬 파이썬과 연동하는 데에 집중했다.
    
    $ 특징
    : ssh 프로토콜 지원
    : sftp 지원
    : 원격지 파이썬의 동기적 구문 실행
    : 원격지 파이썬과 로컬 파이썬 간의 자유로운 변수 교환
    
    $ 주요 용도
    : 파이썬으로 ssh 통신을 보다 쉽게 하고 싶은 경우
    : 원격지 서버의 자원을 빌려야 하는 경우
    : 원격지 서버에서 무거운 프로젝트를, 내 컴퓨터에서 가벼운 클라이언트(혹은 디버거)를 만들고자 할 때
    : 딥러닝 연구 시 원격지 서버에 모델을 실행하면서 이미지 샘플 등을 내 컴퓨터에서 손쉽게 확인하고 싶을 때
    
    $ TODO
    : 원격지 파이썬에서 발생하는 에러를 로컬 파이썬에서 포착할 수 있게 구현할 것
    : @__command__ 함수에 tab 을 입력한 경우 메세지에 입력값이 겹치는 문제를 해결할 것
    
    $ 정보
        @name : Ho Kim
        @github ID : kerryeon
        @email : wwn2856@gmail.com
        @address : 30-416, Gyeongsang National University, Gajwa-dong, Jinju-si, Gyeongsangnam-do, Republic of KOREA
        @version : %s
        @license : LGPL
    
    $ 사용된 모듈
        @python-3.6
        @paramiko
        @numpy - for demo
    
''' % __version_str__


if __name__ == '__main__':
    ''' @EasySSH 클래스
        : 원격지 서버에 ssh 프로토콜로 연결을 시도한다.
        
        @host : 호스트 도메인
        @username : 계정명
        @password : 계정 비밀번호. None 으로 전달 시, 접속 시에 요구한다.
        @port : SSH 프로토콜의 포트
        @connect : 클래스 생성 즉시 연결을 시도할 지 결정한다.
        
    '''
    host = '123.123.123.123'
    username = 'n_a_m_e'
    password = 'p_w'
    port = 22
    connect = True
    ssh = EasySSH(host, username, password, port=port, connect=connect)

    ''' @python 함수 
        : 원격지 서버에 쉘 차원에서 파이썬을 실행한다.
        
        @track : 송수신되는 문자열 데이터를 전부 print 할 지 결정한다.
        
    '''
    py = ssh.python(track=False)

    ''' @import 함수
        : 원격지 파이썬에 모듈을 불러들인다.
        
        @import_from : from ~
        @import_class : import ~
        @import_as : as ~
        
    '''
    py.__import__(import_from='random', import_class='randint', import_as='rand')

    ''' $ 변수 활용법
        : 변수는 원격지 파이썬 객체에 참조 형식으로 접근한 수 있다.
        : 원격지 변수와 로컬 변수 중 일부는 섞어서 사용 가능하다.
        
        $ 자유롭게 변환되는 타입
        : int, float, complex, bool, bytes, str
        
        $ 사용에 제한이 있는 타입
        : 해당 객체의 요소들이 변환 가능해야 한다.
        : list, tuple, dict, set
        
        $ 주의사항
        : 원격지 파이썬에서 발생하는 에러는 로컬 파이썬에서 포착되지 않는다.
        : 차후 추가 예정.
        
    '''
    py.a = [3, 4, 5]

    ''' $ 연산자 활용법
        : 연산자는 ~(invert)를 제외한 기본적인 연산자를 제공한다.
        : ~ 연산자는 특수한 형태로 사용된다.
        
        $ 함수 사용법
        : 함수 또한 일부는 변수처럼 자유롭게 사용할 수 있다.
        
    '''
    py.b = py.a.pop() + py.rand(2, 4) + rand(-4, -2)
    py.b = -py.b
    py.b += 1

    ''' $ 반복문 사용법
        : 반복문은 로컬에서 실행되고, 객체를 매번 받아오는 형식으로 진행된다.
        : 성능에 부정적이므로 가급적 원격지 파이썬을 참조하지 않는 것을 권장한다.
        
        $ 원격지의 변수의 값 불러오기
        : 원격지 파이썬에서 참조하는 원격지 변수 자체는 원격지 변수의 주소만을 가지고 있다.
        : 따라서, 원격지 변수의 값을 로컬로 받아오기 위한 ~ 연산자가 존재한다.
        
    '''
    for a in py.a:
        print(~(a + py.b + 1))

    ''' $ 외부 모듈 불러오기
        : 원격지 파이썬은 원격지 파이썬에 설치된 모듈만 불러올 수 있다.
        : 즉, 로컬 모듈을 직접적으로 참조할 수 없다.
    
    '''
    py.__import__(import_class='numpy', import_as='np')
    py.n = py.np.array([[1, 2], [3, 4]])

    ''' @__download__ 함수
        : 메모리가 큰 원격지 변수를 파일 형식으로 변환하여 받아온다.
        : ~ 연산자에 비해 더 많은 타입을 가질 수 있다. (대부분의 타입)
        : 전송이 완료된 파일은 자동으로 제거된다.
        
        @path : 원격지 서버에 바이너리가 저장될 경로다.
        : 기본값인 None 으로 설정하면, ssh 객체의 경로로 설정된다.
    
    '''
    n = py.n.__download__()

    ''' @__upload__ 함수
        : @__download__ 함수와 반대로, 메모리가 큰 로컬 변수를 파일 형식으로 변환하여 전송한다.
        : 일반적인 연산자에 비해 더 많은 타입을 가질 수 있다. (대부분의 타입)
        : 전송이 완료된 파일은 자동으로 제거된다.
        
        @data : 원격지 서버로 전송할 로컬 변수다.
        @path : 원격지 서버에 바이너리가 저장될 경로다.
        : 기본값인 None 으로 설정하면, ssh 객체의 경로로 설정된다.
    
    '''
    py.c.__upload__(n)
    print(py.c.__download__())

    ''' $ 기타 함수들
    
        $ 원격지 변수
            @__run__ : 원격지 변수가 함수일 경우, 함수를 실행한다.
                     : 기능상으로는 ~ 연산자와 같지만, 변수의 값을 리턴하지 않는다.
                @track : 함수의 진행상황을 print 한다.
                @seconds : @track=True 인 경우, 패킷 업데이트 주기를 결정한다.
            @__addr__ : (property) 원격지 변수의 주소를 반환한다.
        
        $ 원격지 파이썬
            @__def__ : 함수를 실행한다. 참조하기 힘든 원격지 변수를 실행할 때 유용하다.
                     : 값은 메세지인 str 형태로 반환된다.
                @def_name : 함수의 이름이다.
                @*args, **kwargs : 함수의 인자로 들어간다.
            @__command__ : 명령을 실행한다. 참조 형식으로 표현하기 힘든 구문을 실행할 때 유용하다.
                @command : 명령어 구문이다.
                @await : 명령이 완료될 때까지 기다리고 리턴값을 메세지인 str 형태로 받을 지 결정한다.
            @__script__ : 로컬 .py(.pyc) 파일을 원격지에서 import 한다.
                        : 값은 원격지 파이썬에서 import 될 때의 파일명인 str 형태로 반횐된다.
                        $ 주의사항 : 원격지로 파일이 전송될 때 파일명이 임의로 변경되므로, 참조 시 리턴값을 활용한다.
                @lpath : 로컬 파일의 경로다.
                @path : 원격지 서버에 바이너리가 저장될 경로다.
                      : 기본값인 None 으로 설정하면, ssh 객체의 경로로 설정된다.
        
        $ EasySSH 클래스
            @errmsg : (property) 함수가 정상적으로 실행되지 않았을 때의 에러 메세지를 반환한다.
            @path : (property) 현재 참조하고 있는 경로를 반환한다. 경로 이동은 @cd 함수를 이용한다.
            @connect : 원격지 서버에 접속한다. 정상적으로 접속하면 @EasySSH 객체를 반환한다.
            @cd : 경로를 변경한다. 첫문자가 /일 경우 절대경로로, 아닐 경우 상대경로로 이동한다.
            @command : 명령을 실행한다.
                @command : 명령어 구문이다.
                @sudo : root 권한으로 실행할 지 결정한다.
                      : 계정 비밀번호와 root 비밀번호가 다를 경우, init 시 @password 를 None 으로 설정한다.
                @read : 명령이 완료될 때까지 기다리고 리턴값을 메세지인 str 형태로 받을 지 결정한다.
            @close : 접속을 종료한다. 원격지 파이썬과 sftp 통신 등 모든 통신이 종료된다.
            @sftp_open : sftp 통신을 활성화하고 객체를 반환한다. 객체는 @paramiko 에서 확인할 수 있다.
            @sftp_close : sftp 통신을 종료한다. 한 번 종료하면 다시 활성화할 수 없다.
            @get_route : 현재의 경로를 기준으로 주어진 상대경로를 절대경로로 변환한다.
                @path : 참조할 상대경로다.
                $ 주의사항 : /으로 시작하는 경로를 받은 경우 절대경로로 취급한다.

'''
