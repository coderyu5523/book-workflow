package com.metacoding.spring_oauth.post;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface PostRepository extends JpaRepository<Post, Integer> {

    @Query("select p from Post p join fetch p.user order by p.id desc")
    List<Post> findAllWithUser();
}

