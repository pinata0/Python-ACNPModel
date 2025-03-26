---
생성자: Pinata
생성 일시: Invalid date
Resource: https://talkingaboutme.tistory.com/entry/RL-Policy-Gradient-Algorithms
상위 문서:
  - "[[Policy Gradient Theorem]]"
---
**기대보상(Expected Return)** $J(\theta)$

에이전트가 환경에서 행동을 수행할 때 **기대할 수 있는 총 보상의 평균값**

정책 $\pi_\theta$를 따를 때 **미래에 받을 보상의 기대값**

  

수식으로는

$J(\theta)=\mathbb{E}_{\tau\sim\pi_{\theta}}[R(\tau)]$

- $R(\tau)$ : 하나의 trajectory에서 얻은 총 보상
- $\mathbb{E}[\cdot]$ : ~의 기대값
- $\tau\sim\pi_\theta$ : 정책 $\pi_\theta$에 따른 trajectory의 샘플링  
    정책이 stochastic policy라면 행동 $a_t$는 확률적으로 선택  
    정책이 deterministic policy라면 행동 $a_t$는 $\mu_\theta(s_t)$  
    **여러 번 시뮬레이션을 수행하면 서로 다른 trajactory가 나올 수 있음**을 의미