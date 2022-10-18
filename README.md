# Quant_project

## 퀀트기반 추천주 프로그램 - Quant repo를 이어받아, git으로 관리

### 구성
* 데이터 베이스 구성(MySQL)
* DB의 데이터를 전처리 하여 시각화(matplotlib, seaborn)
  * 재무제표 데이터 테이블
  * 날짜별 가격 데이터
    * 수정 주가 테이블
    * 수정전 주가 테이블
  * WICS(국제산업표준)을 기준으로 한 업종코드 테이블
  * 주식 수정 event 발생일 테이블
* 통계를 바탕으로 투자 성과 백테스팅
* 백테스팅 결과 유의미한 결과를 보인 통계 데이터 선택
* 유의미한 통계 데이터를 이용해 인공지능 모델 학습
* 인공지능 모델을 통한 주가 예측
* 주가 예측의 정확도 분석
