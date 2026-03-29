package com.metacoding.websocket.chat;

// 클라이언트가 보낸 채팅 메시지를 REST 바디(JSON)로 받는 DTO
public record ChatRequest(String message) {
}
