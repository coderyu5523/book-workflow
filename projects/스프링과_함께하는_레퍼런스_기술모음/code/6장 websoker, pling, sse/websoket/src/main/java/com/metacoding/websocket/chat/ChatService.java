package com.metacoding.websocket.chat;

import java.util.List;

import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;

@Transactional(readOnly = true)
@RequiredArgsConstructor
@Service
public class ChatService {

    private final ChatRepository chatRepository;

    @Transactional
    public Chat save(ChatRequest req) {
        // 클라이언트가 보낸 메시지를 Chat 엔티티로 만들어 DB에 저장
        Chat chat = Chat.builder().message(req.message()).build();
        return chatRepository.save(chat);
    }
}
