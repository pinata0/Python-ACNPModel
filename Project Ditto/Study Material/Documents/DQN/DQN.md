---
태그:
  - Economic computers
생성자: Pinata
생성 일시: Invalid date
Resource: https://ai-com.tistory.com/entry/RL-%EA%B0%95%ED%99%94%ED%95%99%EC%8A%B5-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-1-DQN-Deep-Q-Network
상위 문서:
  - "[[Q-Learning]]"
하위 문서:
  - "[[Dueling DQN]]"
  - "[[Double DQN]]"
---
> [!important] **DQN (Deep Q-Network)**<br><br>Q-value인 Q(s,a)를 **테이블 형식**으로 저장해 학습하는 기존의 방식
> 
> **state space**와 **action space**가 커지게 되면 모든 Q-value를 저장하기에  
> 많은 메모리와 실행 시간  
> 
> **딥러닝**을 활용해 Q-table에 해당하는 Q-function을 비선형 함수로 근사하는 것.

![[image.png]]

> [!important] **원래 이렇게 하면 문제**
> 
> - 학습의 불안정성
> - 알고리즘의 불수렴성
> 
> **원인**
> 
> - sample correlation
> - data distribution
> - moving target value
> 
> **해결 방법**
> 
> - experience replay
> - target network

# DQN의 구성

> [!important]
> 
> ## CNN Architecture
> 
> CNN의 입력으로 action을 제외한 state만 받고
> 
> **출력으로 action을 나타내는 복수개의 Q value**
> 
> → max Q(s,a) 값을 찾기 위해 CNN을 여러번 통과시키지 않고  
> 먹이기 좋게 CNN 처리된 state를 벨만 방정식에 넣어서 **연산량 감소**

> [!important]
> 
> ## Experience Replay
> 
> Replay memory라는 버퍼를 만들어서 현재 생성된 샘플 저장.
> 
> action을 수행해 결과 값과 샘플을 얻지만 바로 평가에 이용하지 않고 지연.
> 
> ### Experience Replay가 해결하는 문제들
> 
> 1. **Sample correlation**
>     
>     강화학습에서는 연속된 샘플 사이에 **dependency** 존재
>     
>     이전 샘플이 다음 샘플이 생성되는 것에 영향
>     
> 2. **Data distribution**
>     
>     On-policy 학습 모델 : 에이전트가 현재의 policy를 따르면서 학습하는 방식
>     
>     Q-update로 behavior policy가 바뀌면 training data의 분포가 변화한다
>     
>     → 상태 A에서는 행동 B를, 상태 C에서는 행동 D를 선택할 확률이 높아짐.
>     
>     긍정적으로 되면 참 좋겠지만 학습이 잘못되어 **local minimum**에 수렴하거나 발산하게 된다
>     
> 
> **Replay memory**를 이용해서 랜덤하게 추출된 샘플들은  
> 각각 다른 시간에서 수행된 샘플들  
> → **sample correlation**이 작다.

> [!important]
> 
> ## Target Network
> 
> Target Network는 Main Q-network의 사본  
> → 모델을 고정시키는 역할  
> → Q-update가 불안정해지지 않도록  
> 
>   
> 
> **Target value**
> 
> $y_j = r_j + \gamma max_{a’} Q(s_{j+1}, a’; \theta ^-)$
> 
> - $r_j$ : 현재 시간 j에서 받은 보상
> - $\gamma$ : 할인률
> - $max_{a'} Q(s_{j+1}, a’; \theta ^-)$ : 다음 상태에서 가능한 최대 Q-value
> - $\theta ^-$ : Target network의 파라미터
> 
>   
> 
> **Main Q-network :** 실제로 행동을 선택하고 Q-value를 추정하는 네트워크
> 
> $Q(s_j,a_j;\theta )$
> 
> - $s_j$ : 현재 상태
> - $a_j$ : 현재 상태에서 선택된 행동
> - $\theta$ : Main Q-network의 파라미터
> 
>   
> 
> **Loss Function**
> 
> $Loss = (y_j - Q(s_j, a_j ; \theta ))^2$ ~~(MSE…)~~
> 
> → **Loss의 차이를 최소화**하는 방향으로 $\theta$를 변화시키며 학습이 이루어짐
> 
> → 매 C 스텝마다 Target Network parameter($\theta^-$)는 Main Q-Network parameter($\theta$)로 덮어씌우기
> 
>   
> 
> ### Target Network가 해결하는 문제들
> 
> 1. **Moving target value**
>     
>     Q-learning은 업데이트시 결과값인 action-value와 target-value가 같이 움직인다.
>     
>     → AI : 지금이 가장 낮은 곳 아님?
>     
> 
>   
> 
> **Target Network**를 통해 해당 구간 동안은 원하는 방향으로 모델을 업데이트
> 
> → bias를 줄인다