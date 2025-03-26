---
생성자: Pinata
생성 일시: Invalid date
상위 문서:
  - "[[DQN]]"
---
**Dueling DQN** : 강화학습에 더 특화된 신경망 구조

  

**DQN의 경우**

CNN 끝나자마자 Q-value를 추정한다

  

**Dueling DQN의 경우**

Fully-connected layer를 두 부분으로 분리하여  
State-value와 Advantage로 나누어 추정한 후 마지막에 합쳐 Q-value를 출력  

  

**State-value function V(s)**

현재 state의 가치를 표현  
앞으로 선택될 action과는 상관이 없다.  

  

**Advantage function A(s,a)**

현재 state에서 해당 action이 다른 action에 비해 가지는 상대적인 가치

$A(s,a) = Q(s,a) - V(s)$

  

**합치는 방식**

$Q(s,a) = V(s) + (A(s, a) - \underset{a’\in|\mathcal{A}|}{max}A(s,a’))$

아니면

$Q(s,a) = V(s) + (A(s,a) - \frac{1}{\mathcal{|A|}}\sum\limits_{a’}A(s,a’))$

최댓값 대신 평균을 이용하면 정확한 state-value는 못 가지겠지만  
advantage의 변화량이 적어 학습 안정성이 올라가는 효과  

  

**효과 → 불필요한 행동까지 학습하지 않아도 된다.**

즉, 공통적인 상태가치와 행동 이점을 따로 예측한다.

불필요한 행동 학습을 피하고, **중요한 상태**에 집중할 수 있다.