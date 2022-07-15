<div align="center">

  # 과제 03 - GameDuo_Backend

</div>


## 목차
- [F팀 멤버 소개](#-team-f-member)  
- [개발 기간](#--개발-기간--)  
- [프로젝트 설명 분석](#-프로젝트)
- [개발 조건](#-개발-조건)
- [실행방법](#실행-방법)
- [배포](#-배포)
- [swagger](#swagger)  
- [테스트 케이스](#테스트-케이스)  
- [기술 스택](#기술-스택) 
<br><br>
<div align="center">

## 👨‍👨‍👦‍👦 Team "F" member  

|                이승민                 |                 임혁                  |                 전재완                  |                 정용수                 |
| :-----------------------------------: | :-----------------------------------: | :-------------------------------------: | :------------------------------------: |
| [Github](https://github.com/SMin1620) | [Github](https://github.com/Cat-Nile) | [Github](https://github.com/iamjaewhan) | [Github](https://github.com/blueknarr) |

  <br>

| <img height="200" width="380" src="https://retaintechnologies.com/wp-content/uploads/2020/04/Project-Management-Mantenimiento-1.jpg"> | <img height="200" width="330" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGElLjafMUhHglmqwh9lRh_sVzOCQyBiPNfQ&usqp=CAU"> |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| 💻 [**Team work**](https://www.notion.so/Team-F-3f553f413ee14b389da0641d8bb4d99e) | 📒 [**Project page**](https://www.notion.so/21776eb6eb77429b9c9b4e65509c6aa5) |
|        공지사항, 컨벤션 공유 등<br> 우리 팀을 위한 룰        | 요구사항 분석, 정보 공유 및<br> 원할한 프로젝트를 위해 사용  |
 <br>
  </div> 

  <h2> ⌛ 개발 기간  </h2> 
 2022/07/11  ~ 2022/07/15
 <br><br>
  </div> 


# 💻 프로젝트
  ### 프로젝트 설명
  - 보스레이드 PVE 컨텐츠 관련 6가지 라우터를 작성해주세요. 
      - 유저 생성
      - 중복되지 않는 userId 생성
          - 생성된 userId 응답
      - 유저 조회
      - 해당 유저의 보스레이드 총 점수와 참여기록 응답
      - 보스레이드 상태 조회
          - 보스레이드 현재 상태 응답
              - canEnter: 입장 가능 여부
              - enteredUserId: 현재 진행중인 유저가 있다면, 해당 유저의 id
          - 입장 가능 조건: 한번에 한명의 쥬저만 보스레이드 진행, 레이드 제한 시간 고려
      - 보스 레이드 시작
          - 중복되지 않는 raidRecordId를 생성 후 isEntered:true 응답
          - 시작이 불가능 하다면 isEntered: false
      - 보스레이드 종료
          - 레이드 level에 따른 score 반영
          - 유효성 검사: userId와 raidRecordId가 일치하지 않다면 예외 처리
          - 시작한 시간으로부터 레이드 제한 시간이 지났다면 예외처리
      - 보스레이드 랭킹 조회



  ### 프로젝트 분석

  - Static Data를 Redis에 캐싱하여 사용
  - 보스레이드 입장 제한 시간에 따라 재입장 처리
  - 저장된 userId와 raidRecordidId 일치하지 않다면 예외 처리
  - 동시성 고려
      - 유저A와 유저B가 같은 보스레이드에 입장했을 때 처리
  -  랭킹 데이터는 웹 서버에 캐싱 또는 Redis에 캐싱
  -  레이어 계층 분리
  -  발생할 수 있는 다양한 예외 처리



### API 명세서

| ID   | URI                     | METHOD | 기능                 |
| ---- | ----------------------- | ------ | -------------------- |
| 1    | /user                   | POST   | 유저 생성            |
| 2    | /user/<int: user_id>    | GET    | 유저 조회            |
| 3    | /bossRaid               | GET    | 보스레이드 상태 조회 |
| 4    | /bossRaid/enter         | POST   | 보스레이드 시작      |
| 5    | /bossRaid/end           | PATCH  | 보스레이드 종료      |
| 6    | /bossRaid/topRankerList | GET    | 랭킹조회             |

### ERD

사진
<br><br>
</div>




  ### 🚥 개발 조건 

  #### 🙆‍♂️ 필수사항  
    - Python, Django
    - Static Data Redis 캐싱
    - 동시성 고려
    - 레이어 계층 분리
  #### 🔥 선택사항
    - Docker
    - Unit test codes  
    - REST API Documentation (Swagger UI)  





## 실행 방법

```
📌 Dependency

# 로컬에서 바로 서버 구동
pip install -r requirements.txt
python manage.py runserver

# 도커 실행
pip install docker
pip install docker-compose
docker-compose up -d

(장고 서버는 15초 대기 시간을 걸었습니다.)
```





## 🔥 배포

docker를 이용해 프로젝트 api를 컨테이너화 하여 GCP에 배포했습니다  

[API Link]()

GCP 배포, 테스트 및 동작을 확인하였으며, 비용 등의 이유로 현재는 접속불가할 수 있습니다.
<br><br>



## swagger

[API 명세서 (Swagger)]()

<br><br>



## 테스트 케이스

Pytest-Django로 구현 된 개의 테스트 구현

- 성공 케이스: 개 (통과)
- 실패 케이스: 개 (통과)  
<br><br>



## 기술 스택

> - Back-End :  <img src="https://img.shields.io/badge/Python 3.10-3776AB?style=flat&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 4.0.4-092E20?style=flat&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django-DRF 3.13.1-009287?style=flat&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker 20.10.14-2496ED?style=flat&logo=docker&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Nginx-009639?style=flat&logo=Nginx&logoColor=white"/>
>
> - ETC　　　:  <img src="https://img.shields.io/badge/Git-F05032?style=flat-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=flat-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Swagger-FF6C37?style=flat-badge&logo=Swagger&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white"/>
