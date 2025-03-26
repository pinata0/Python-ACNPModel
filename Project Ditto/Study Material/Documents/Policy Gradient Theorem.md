---
생성자: Pinata
생성 일시: Invalid date
Resource: https://talkingaboutme.tistory.com/entry/RL-Policy-Gradient-Algorithms
상위 문서:
  - "[[Policy Gradient Algorithm]]"
하위 문서:
  - "[[Differentiation of Expected Compensation]]"
  - "[[Deterministic Policy]]"
  - "[[Expected Return]]"
---
**Policy Gradient Theorem = 정책 기울기 정리**

  

**기대보상** $J(\theta)$에게

$J(\theta)=\mathbb{E}_{\tau\sim\pi{\theta}}[R(\tau)]$

  

**기대보상의 기울기**

$\nabla_\theta J(\theta) = \nabla_\theta \mathbb{E}_{\tau\sim\pi_\theta} [R(\tau)]$

  

**미분하면**

$\nabla_\theta J(\theta) = \mathbb{E}_{\tau\sim\pi\theta} [R(\tau)\nabla_\theta \log P(\tau)]$

  

어떤 trajectory의 **확률** $P(\tau)$를 **정책** $\pi_\theta$**와 상태 전이 확률** $P(s'|s,a)$**로 나눠** 표현할 때

$P(\tau) = P(s_0) \prod\limits_{t=0}^{T} \pi_\theta (a_t|s_t)P(s_{t+1}|s_t, a_t)$

$\log P(\tau) = P(s_0) \sum\limits_{t=0}^{T} \log\pi_\theta (a_t|s_t) \sum\limits_{t=0}^{T}\log P(s_{t+1}|s_t, a_t)$

  

**상태 전이 확률은** $\theta$**와 무관**하므로 **미분하면 0**이 되어

$\nabla_\theta \log P(\tau) = \sum\limits_{t=0}^{T} \nabla_\theta \log \pi_\theta (a_t|s_t)$

$\nabla_\theta J(\theta) = \mathbb{E}_{\tau\sim\theta} [\sum\limits_{t=0}^{T} \nabla_\theta \log \pi_\theta (a_t|s_t) R_t]$