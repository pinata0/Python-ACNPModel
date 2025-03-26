---
태그:
  - Economic computers
생성자: Pinata
생성 일시: Invalid date
하위 문서:
  - "[[Policy Gradient Theorem]]"
  - "[[Reinforce Algorithm]]"
  - "[[TD]]"
  - "[[MDP]]"
---
**Policy Gradient Algorithm**

정책 $\pi_\theta$를 바꿔가며 기대보상 $J(\theta)$를 최대화하는 과정

  

이를 위해 사용하는 **Gradient Ascent(경사상승법)**

  

**Policy Gradient Theorem**에 따라 기대보상의 기울기는

$\nabla_\theta J(\theta) = \mathbb{E}_{\tau\sim\theta} [\sum\limits_{t=0}^{T} \nabla_\theta \log \pi_\theta (a_t|s_t) R_t]$

  

이를 따라 Policy를 학습률 $\alpha$를 통해 gradient ascent로 업데이트 할 수 있다.

$\theta ← \theta + \alpha \nabla_\theta J(\theta)$