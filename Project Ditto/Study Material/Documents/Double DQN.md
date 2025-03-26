---
생성자: Pinata
생성 일시: Invalid date
Resource: https://ai-com.tistory.com/entry/RL-%EA%B0%95%ED%99%94%ED%95%99%EC%8A%B5-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-2-Double-DQN
상위 문서:
  - "[[DQN]]"
---
**Double DQN** : Target value가 처음부터 잘못된 경우 예외처리

Target value가 처음부터 잘못되어 있으면 보통 overestimate 된다.

  

**DQN의 경우**

$y_t = r_t + \gamma max_a Q_{target}(s_{t+1}, a; \theta^-)$

원래는 Target Q-value 계산할때 다음 상태에서 최대 Q 값을 가진 행동을 선택한다.  
같은 네트워크에서 행동 선택과 평가를 수행해서 과적합 되는 문제가 있었다.  

  

**Double DQN의 경우**

$y_t = r_t + \gamma Q_{target}(s_{t+1}, argmax_{a'}~ Q_{online}(s_{t+1}, a; \theta); \theta-)$

  

**Online Q-network** : 매 스탭마다 업데이트

두 network를 분리함으로써  
Online Q-network에서 행동을 선택하고  
Target Q-network에서 Q 값을 평가한다  

**→ action의 selection과 evalutation의 분리**

→ 현재 state의 가치 추정 방지

  

추가로

**Soft Update**

$\theta_{target} ←\tau\theta_{online} + (1-\tau)\theta_{target}$  
$\tau$는 0~1 사이의 값