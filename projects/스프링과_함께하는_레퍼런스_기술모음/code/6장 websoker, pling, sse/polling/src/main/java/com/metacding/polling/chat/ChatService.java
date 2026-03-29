package com.metacding.polling.chat;

import java.util.List;

import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class ChatService {

    private final ChatRepository chatRepository;

    // POST /chats에서 들어온 메시지를 저장
    @Transactional
    public Chat save(ChatRequest req) {
        Chat chat = Chat.builder()
                .message(req.message())
                .build();
        return chatRepository.save(chat);
    }

    // 폴링 요청 시 최신순으로 전체 메시지 조회
    public List<Chat> findAll() {
        Sort desc = Sort.by(Sort.Direction.DESC, "id");
        return chatRepository.findAll(desc);
    }
}
