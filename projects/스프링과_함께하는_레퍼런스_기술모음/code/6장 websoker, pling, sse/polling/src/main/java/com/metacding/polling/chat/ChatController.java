package com.metacding.polling.chat;

import java.util.List;

import org.springframework.http.ResponseEntity;
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

    @GetMapping("/")
    public String index() {
        return "index";
    }

    /*
     * 메세지 저장
     */
    @PostMapping("/chats")
    @ResponseBody
    public ResponseEntity<Chat> save(@RequestBody ChatRequest req) {
        Chat saved = chatService.save(req);
        return ResponseEntity.ok(saved);
    }

    /*
     * 메세지 list조회
     */
    @GetMapping("/chats")
    @ResponseBody
    public ResponseEntity<List<Chat>> list() {
        List<Chat> chats = chatService.findAll();
        chats.forEach(chat -> {
            System.out.println("id=" + chat.getId() + ", msg=" + chat.getMessage());
        });
        return ResponseEntity.ok(chats);
    }
}
