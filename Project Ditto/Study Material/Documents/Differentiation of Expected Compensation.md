---
생성자: Pinata
생성 일시: Invalid date
상위 문서:
  - "[[Policy Gradient Theorem]]"
---
기대보상 $J(\theta)$이 있을 때,

$J(\theta)=\mathbb{E} _ {\tau \sim \pi_ \theta}[R(\tau)]$

미분하면

$\nabla_\theta J(\theta) = \nabla_\theta \sum\limits_\tau P(\tau) R(\tau)$

  

> [!important] **로그 미분 트릭(Log Derivative Trick)**
> 
> 어떤 확률 밀도 함수 $P(x)$가 있을 때,
> 
> $\nabla_\theta P(x) = P(x) \nabla_\theta \log P(x)$
> 
> $\nabla_\theta P(\tau) = P(\tau) \nabla_\theta \log P(\tau)$
> 
> 으로 표현할 수 있다.

  

정리하면

$\nabla_\theta J(\theta) = \sum\limits_\tau \nabla_\theta P(\tau) R(\tau) = \sum\limits_\tau P(\tau)\nabla_\theta \log P(\tau) R(\tau)$

$\nabla_\theta J(\theta) = \mathbb{E}{\tau\sim\pi\theta} [R(\tau)\nabla\theta \log P(\tau)]$