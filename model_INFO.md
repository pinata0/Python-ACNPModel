# Model
Input : 사건 키워드, 기업들 주가 등의 TSD
Output : 사건 및 기존 주가 흐름에 의해 예측된 각 기업들의 주가 map
Trajectory : walk-forward validation
Solution : (기업명, 사건 키워드) 쌍이 다른 기업의 flow 영향률

# 정리
n번째 날에 대해서

Input :
1.
기업 A, B, C, D...의
n-1일까지의 사건 일으킨 기업, 그 사건의 keyword
형태로 써진 그 일자 일어난 모든 사건 리스트
2.
n-1일까지의 기업 B 주가 시계열 데이터

Output : 
기업 B의 flow 영향률

# 수학적 정리
Input :
1. 사건 정보 리스트
$Events_{<n} = {(c_i, k_i) | 기업 c_i가 일으킨 사건 키워드 k_i}$
각 사건은 기업 ID와 키워드로 구성
예 : [(A, "공매도"), (C, "배당 확대"), ...]

2. 기업 B의 시계열 데이터
$Price_B^(t) for t = 1 to n-1$

Output : 
기업 B의 flow 영향률
$\Delta y^{(n)}_B = y^{(n)}_B - y^{(n-1)}_B$

다중 이벤트 기반 외생 요인 영향 추정 시계열 예측 문제