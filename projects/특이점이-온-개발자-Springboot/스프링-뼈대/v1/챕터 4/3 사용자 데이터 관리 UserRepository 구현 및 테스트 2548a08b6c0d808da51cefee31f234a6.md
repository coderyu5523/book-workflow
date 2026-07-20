# 3. 사용자 데이터 관리: UserRepository 구현 및 테스트

# 3.1 회원가입

user 폴더에 UserRepository.java 파일을 생성합니다.

**src > main > java > com > metacoding > springv1 > user**

![**1.png**](3%20%EC%82%AC%EC%9A%A9%EC%9E%90%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B4%80%EB%A6%AC%20UserRepository%20%EA%B5%AC%ED%98%84%20%EB%B0%8F%20%ED%85%8C%EC%8A%A4%ED%8A%B8/image.png)

**1.png**

다음과 같이 em.persist를 사용하여 User 엔티티를 저장하는 save 메서드를 구현합니다.

**UserRepository.java**

```java
package com.metacoding.springv1.user;

import org.springframework.stereotype.Repository;
import java.util.Optional;
import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class UserRepository {

    public final EntityManager em;

    public void save(User user){
        em.persist(user);   
    }
}
```

# 3.2 아이디로 사용자 조회

아래와 같이 JPQL 문법을 활용하여 findByUsername 메서드를 구현합니다.
이 메서드는 지정한 사용자명을 조건으로 User 엔티티를 조회 후 Optional 타입으로 반환합니다.

**UserRepository.java**

```java
public Optional<User> findByUsername(String username) {
    Optional<User> user = em.createQuery("select u from User u where u.username = :username", User.class)
            .setParameter("username", username)
            .getResultStream()
            .findFirst();
    return user;
}
```

# 3.3 테스트 진행

이제 테스트를 진행해보겠습니다.

test 디렉터리 내에 user 패키지를 생성한 후, 그 안에 UserRepositoryTest.java 클래스를 생성합니다.

**test > java > com > metacoding > springv1 >user**

![**2.png**](3%20%EC%82%AC%EC%9A%A9%EC%9E%90%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B4%80%EB%A6%AC%20UserRepository%20%EA%B5%AC%ED%98%84%20%EB%B0%8F%20%ED%85%8C%EC%8A%A4%ED%8A%B8/image%201.png)

**2.png**

그리고 UserRepositoryTest 를 구현합니다.

**UserRepositoryTest**

```java
package com.metacoding.springv1.user;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@Import(UserRepository.class)
@DataJpaTest
public class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;
    
}
```

## 3.3.1 회원가입

userRepository에 생성한 메서드를 호출해보겠습니다.

**UserRepositoryTest**

```java
@Test
public void save_test(){
    //given
    User user = User.builder()
           .username("user1")
           .password("1234")
           .email("user1@metacoding.com")
           .build();
    //when
    userRepository.save(user);
    //eye
    System.out.println("=======================");
    System.out.println("id : " + user.getId());
    System.out.println("username : " + user.getUsername());
    System.out.println("email : " + user.getEmail());
}
```

테스트를 실행하면 콘솔에 INSERT 쿼리가 실행되며, 이를 통해 데이터가 정상적으로 저장된 것을 확인할 수 있습니다.

![**3.png**](3%20%EC%82%AC%EC%9A%A9%EC%9E%90%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B4%80%EB%A6%AC%20UserRepository%20%EA%B5%AC%ED%98%84%20%EB%B0%8F%20%ED%85%8C%EC%8A%A4%ED%8A%B8/image%202.png)

**3.png**

## 3.3.2 아이디로 사용자 조회

다음과 같이 테스트를 진행합니다.

**UserRepositoryTest**

```java
@Test
public void findByUsername_test(){
    //given
    String username = "ssar";
    //when
    User user = userRepository.findByUsername(username).get();
    //eye
    System.out.println("=======================");
    System.out.println("id : " + user.getId());
    System.out.println("username : " + user.getUsername());
    System.out.println("email : " + user.getEmail());
}
```

username을 조건으로 한 SELECT 쿼리가 실행되며, 더미 데이터에 저장된 회원 정보가 정상적으로 조회됩니다.

![**4.png**](3%20%EC%82%AC%EC%9A%A9%EC%9E%90%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B4%80%EB%A6%AC%20UserRepository%20%EA%B5%AC%ED%98%84%20%EB%B0%8F%20%ED%85%8C%EC%8A%A4%ED%8A%B8/image%203.png)

**4.png**