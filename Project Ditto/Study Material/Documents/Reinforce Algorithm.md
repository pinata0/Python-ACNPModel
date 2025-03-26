---
생성자: Pinata
생성 일시: Invalid date
Resource: https://yscho.tistory.com/114
상위 문서:
  - "[[Policy Gradient Algorithm]]"
하위 문서:
  - "[[Advantage Actor-Critict]]"
  - "[[Reinforce Algorithm Code]]"
  - "[[DDPG]]"
---
**Reinforce Algorithm**

- 가장 기본적인 Policy Gradient Algorithm
- 환경과 상호작용하며 **Monte Carlo 방식**으로 학습
- **Value Function 없이** 정책만으로 학습
- 행동을 **확률적으로 선택**

  

**환경 수집 과정**

- 초기 상태 $s_0$에서 시작
- 정책 $\pi_\theta(a|s)$에 따라 행동 선택
- 보상 $r_t$를 받고 새로운 상태 $s_{t+1}$로 이동
- 한 에피소드가 끝날 때까지 반복

  

**장점**

- 정책을 직접 학습하므로 **고차원 연속 행동 공간에서도 사용 가능**
- 확률적으로 행동을 선택하여 **탐색 문제를 해결**
- 현재 정책을 직접 학습해 **On-policy 학습 가능**

  

**단점**

- High Variance
- Sample Inefficiency
- Credit Assignment
    - 보상을 받을 때 어떤 행동이 얼마나 기여했는지 불분명