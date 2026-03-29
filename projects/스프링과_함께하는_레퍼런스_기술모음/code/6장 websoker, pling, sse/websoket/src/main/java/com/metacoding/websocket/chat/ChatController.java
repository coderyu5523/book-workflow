package com.metacoding.websocket.chat;

import java.util.List;

import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Controller
public class ChatController {

    private final ChatService chatService;
    private final SimpMessagingTemplate messagingTemplate;

    @GetMapping("/")
    public String index() {
        return "index";
    }

    // WebSocketConfig의 setApplicationDestinationPrefixes("/app") 때문에
    // 클라이언트는 /app/chats 로 SEND하고, 브로커는 /topic/chats 로 구독합니다.
    @MessageMapping("/chats")
    public void handle(ChatRequest payload) {
        Chat saved = chatService.save(payload);
        messagingTemplate.convertAndSend("/topic/chats", saved);
    }

}
