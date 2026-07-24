package com.metacoding.spring.reply;

import org.springframework.stereotype.Repository;

import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;
import java.util.Optional;

@RequiredArgsConstructor
@Repository
public class ReplyRepository {
    private final EntityManager em;

    public void save(Reply reply) {
        em.persist(reply);
    }

    public Optional<Reply> findById(Integer replyId) {
        return Optional.ofNullable(em.find(Reply.class, replyId));
    }

    public void delete(Reply reply) {
        em.remove(reply);
    }
}
