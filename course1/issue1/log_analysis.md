# 미션 로그 분석 보고서
## 1. 사고 개요
- 발생시간 : 2023-08-27 11:35 ~ 11:40
- 사유 : 산소 탱크 폭발
### 영향 : 
- 로켓이 11:28에 착륙 후 11:30에 미션 완료
- 그러나 11:35에 산소 탱크가 불안정해짐짐
- 11:40에 폭발 발생
- 12:00에 모든 시스템이 종료됨

## 2. 로그 분석
- 10:00 >> 발사 준비(로켓 초기화 시작)
- 10:30 >> 이륙(로켓 발사됨)
- 10:57 >> 궤도 진입(로켓이 계획된 궤도에 진입)
- 11:05 >> 미션 성공(위성 배포 성공)
- 11:28 >> 착륙 완료

### 사고 발생 구간
- 11:35 >> 산소탱크 불안정
- 11:40 >> 산소 탱크 폭발 발생
- 12:00 >> 시스템 종료료

## 3. 사고 원인 분석

- 산소 탱크 불안정 (11:35) → 탱크 압력 이상 가능성
- 5분 후 폭발 (11:40) → 압력 상승 → 폭발
- 시스템 종료 (12:00) → 폭발로 인해 미션 컨트롤 시스템 종료