---
태그:
  - Economic computers
생성자: Pinata
생성 일시: Invalid date
Resource: https://velog.io/@yookyungkho/%EB%94%A5%EB%9F%AC%EB%8B%9D-%EC%98%B5%ED%8B%B0%EB%A7%88%EC%9D%B4%EC%A0%80-%EC%A0%95%EB%B3%B5%EA%B8%B0%EB%B6%80%EC%A0%9C-CS231n-Lecture7-Review
---
**딥러닝에서 모델을 학습 = 최적화(Optimization) task를 수행**

  

**Optimization**

- **손실함수의 최솟값**을 찾는 것
- **역전파(Backpropagation) 과정** 중에 가중치를 업데이트
    
    - 한 스텝마다 이동하는 발자국의 크기**(보폭)**이 **학습률**
    - 앞으로 이동할 **방향**은 현 지점의 기울기**(gradient)**를 통해 정의
    
      
    

> [!important] **SGD(Stochastic Gradient Descent)**
> 
> - 기존 Batch Gradient Descent
>     - 한 번 학습할 때 모든 학습 데이터를 가지고 연산을 진행
>     - 연산량이 많아 학습 속도가 느림
> - Stochastic Gradient Descent
>     - 한 번에 전체 학습데이터에서 하나씩 랜덤으로 뽑아 학습을 진행
>     - Mini-batch Stochastic GD
>         - 하이퍼파라미터로 정의된 batch_size만큼의 데이터를 랜덤으로 뽑아 한 회 학습에 이용
>     - 빠르게 학습되지만, 지그재그로 핑퐁하면서 불안정한 학습과정
>     - Local minima, Saddle point에 빠짐

  

> [!important] **Momentum**