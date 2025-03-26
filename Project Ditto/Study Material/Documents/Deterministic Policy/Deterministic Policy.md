---
생성자: Pinata
생성 일시: Invalid date
Resource: https://ai-com.tistory.com/entry/RL-%EA%B0%95%ED%99%94%ED%95%99%EC%8A%B5-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-4-DDPG
상위 문서:
  - "[[Policy Gradient Theorem]]"
---
### 기존의 DPG 알고리즘

**Stochastic policy** 알고리즘 $\pi(a|s)$는 모든 action에 대한 확률 분포를 가진다.

즉, 주어진 상태 $s$에서 행동 $a$를 취할 확률 분포를 나타낸다.

![[image 2.png|image 2.png]]

**Deterministic policy** 알고리즘 $\mu(a)$는 하나의 action에 대한 확률 분포를 가진다.

즉, 특정 상태에서 항상 하나의 행동만 선택하는 경우다.

![[image 1.png]]

**Deterministic policy**는 action을 **parameterize** 할 수 있으며 **continuous action**을 나타낼 수 있는 장점이 있다.

  

**Stochastic policy**

행동 $a$가 확률 분포에서 샘플링되므로, 일반적으로 action state가 discrete할 때 주로 사용된다. 그러나 그러지 않는 경우가 있다.

  

자동차의 가속도를 [-1, 1] 사이의 연속적인 값으로 조정해야 한다고 하자.

이를 discrete한 값으로 변환하면

**Binning** 방식의 경우

$[-1.0,~ -0.5,~ 0.0,~ 0.5,~ 1.0]$

**Multi-discrete** 방식의 경우

$악셀 \in [0,~1,~2,~3], ~브레이크 \in [0,~1,~2,~3]$

이와 같이 연속 행동을 흉내낼 수 있긴 한데, 세밀한 조정이 어렵다.

  

**Deterministic policy**

그래서 모델이 직접 **행동을 매핑하는 함수**를 설정하자는 아이디어가 생겼다.

이제 연속적인 행동 공간에서 연속적인 행동 값을 출력할 수 있다.