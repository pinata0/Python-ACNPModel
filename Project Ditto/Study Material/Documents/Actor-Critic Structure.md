---
생성자: Pinata
생성 일시: Invalid date
Resource: https://qcoding.tistory.com/77
상위 문서:
  - "[[Advantage Actor-Critict]]"
---
**Actor-Critic 구조**

- **행동 가치**
    - 하나의 Episode에서 받는 reward의 총 합 $G_t$를 정의했을 때
        
        $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + … = \sum\limits_{k=0}^{\infty} \gamma^k R_{t+k+1}$
        
    - 정책 $\pi$ 하에서 **특정 상태** $s$ **행동** $a$**의 경우**, 기대되는 미래 누적 보상
        
        $Q_\pi(s,a) = \mathbb{E}_\pi [G_t | S_t = s, A_t = a]$
        
    - Bellman Expectation Equation
        
        $Q_\pi(s,a) = \mathbb{E}[r + \gamma Q_{\pi}(s', a')| S_t = s, A_t = a]$
        

  

- **상태 가치**
    - 하나의 Episode에서 받는 reward의 총 합 $G_t$를 정의했을 때
        
        $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + … = \sum\limits_{k=0}^{\infty} \gamma^k R_{t+k+1}$
        
    - 정책 $\pi$ 하에서, **특정 상태** $s$**의 경우 기대되는** 미래 누적 보상
        
        $V_\pi(s) = \mathbb{E}_\pi [G_t|S_t = s]$
        
    - Bellman Expectation Equation
        
        $V_\pi(s) = \mathbb{E}_\pi [r+\gamma V_\pi (s')|S_t = s]$
        
    - MDP 상에서 행동 선택이 확률적으로 이루어질 경우
        
        $V_\pi(s) = \sum\limits_a \pi(a|s) \sum\limits_{s'}P(s'|s,a)[r+\gamma V_\pi(s')]$