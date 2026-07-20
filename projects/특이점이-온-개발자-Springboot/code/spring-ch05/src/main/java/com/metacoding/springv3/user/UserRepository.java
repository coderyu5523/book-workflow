package com.metacoding.springv3.user;

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

    public Optional<User> findByUsername(String username){
        return em.createQuery("select u from User u where u.username = :username", User.class)
                          .setParameter("username", username)
                          .getResultStream()
                          .findFirst();
  }
}