package com.metacoding.spring.user;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.context.annotation.Import;

@Import(UserRepository.class)
@DataJpaTest
public class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

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

}