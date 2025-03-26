---
생성자: Pinata
생성 일시: Invalid date
Resource: https://velog.io/@chulhongsung/A2CAdvantage-Actor-Critic-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98
상위 문서:
  - "[[Reinforce Algorithm]]"
하위 문서:
  - "[[A2C]]"
  - "[[Actor-Critic Structure]]"
  - "[[A3C]]"
---
**Policy Gradient Algorithm**은

$\nabla_\theta J(\theta) = \mathbb{E}_{\tau\sim\pi_\theta} [\sum\limits_{t=0}^{T} \nabla_\theta \log \pi_\theta (s_t|a_t) R_t]$

  

두 가지 문제가 있다.

- **High Variance** : 보상 $R_t$가 크면 학습이 불안정해진다.
- **Sample Inefficiency** : Policy를 업데이트하기 위해 많은 샘플이 필요하다.

  

- **Actor (행동자)**
    - Policy $\pi_\theta(a|s)$를 담당하는 신경망
    - Policy Gradient 방식으로 학습
    - **어떤 행동을 할지 결정**

  

- **Critic (비평자)**
    - 가치 함수 $V(s)$를 학습하는 신경망
    - 보상을 예측하여 Actor의 학습을 보조
    - **현재 상태가 얼마나 좋은지 평가**

  

Actor-Critic의 산출물로 나오는 **Advantage 함수**

$A(s,a) = Q(s,a) - V(s)$

- $Q(s,a)$ : 상태 s에서 행동 a를 했을 때 예상 총 보상
- $V(s)$ : 현재 상태 s의 가치

  

$\nabla_\theta J(\theta) = \mathbb{E}_{\tau\sim\pi_\theta} [\sum\limits_{t=0}^{T} \nabla_\theta \log \pi_\theta (a_t|s_t) A(s_t,a_t)]$

보상을 Advantage 함수로 대체함으로써 **불필요한 업데이트를 줄인다**.

**정책(Actor)와 가치(Critic)를 동시에 학습**하여 더 안정적이고 빠르게 최적의 정책을 찾는 강화학습