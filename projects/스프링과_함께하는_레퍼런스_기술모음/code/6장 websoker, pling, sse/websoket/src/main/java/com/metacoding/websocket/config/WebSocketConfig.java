package com.metacoding.websocket.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

// 메시지 브로커
@EnableWebSocketMessageBroker
@Configuration
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    /**
     * WebSocket 연결 엔드포인트 설정
     *
     * 클라이언트에서
     * "/ws" 로 WebSocket Handshake 를 시도한다.
     *
     * 여기서는 단순히 "연결 지점"만 잡는 것이고,
     * 실제 메시지 라우팅은 configureMessageBroker 에서 prefix 로 나눈다.
     */
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
                .setAllowedOriginPatterns("*");
    }

    /**
     * STOMP 메시지 브로커 설정
     *
     * 1) enableSimpleBroker("/topic")
     * - "브로커가 직접 처리하는 목적지(prefix)" 를 의미한다.
     * - destination 이 "/topic" 으로 시작하면 SimpleBroker 가 바로 응답을 보낸다.
     * 
     * 예) messagingTemplate.convertAndSend("/topic/chats", payload)
     * → @MessageMapping 을 거치지 않고,
     * "/topic/chats" 를 SUBSCRIBE 한 모든 클라이언트에게 즉시 PUSH.
     *
     * 2) setApplicationDestinationPrefixes("/app")
     * - "스프링 애플리케이션으로 보내는 목적지(prefix)" 를 의미한다.
     * - 클라이언트가 SEND 할 때 destination 이 "/app" 으로 시작하면
     * SimpleBroker 로 가지 않고, 먼저 스프링 메시지 핸들러(@MessageMapping) 로 들어간다.
     * 예) 클라이언트: SEND /app/chats
     * → 서버: @MessageMapping("/chats") 메서드 호출
     *
     * 정리하면:
     * - /app 로 시작하는 주소 → 스프링 컨트롤러(@MessageMapping)를 "타고" 들어감
     * - /topic 로 시작하는 주소 → SimpleBroker 가 "바로" 구독자에게 브로드캐스트
     *
     * 실제 채팅 흐름 예:
     * 1) 브라우저: SEND "/app/chats" (메시지 전송)
     * 2) 서버: @MessageMapping("/chats") 에서 DB 저장 등 비즈니스 로직 실행
     * 3) 서버: messagingTemplate.convertAndSend("/topic/chats", savedChat)
     * 4) 브로커: "/topic/chats" 구독자들에게 MESSAGE 프레임 PUSH
     */
    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        // 서버 → 클라이언트 방향 브로드캐스트 주소(prefix)
        // "/topic" 로 시작하는 목적지는 SimpleBroker 가 처리한다.
        registry.enableSimpleBroker("/topic");

        // 클라이언트 → 서버 방향 애플리케이션 주소(prefix)
        // "/app" 으로 시작하는 목적지는 @MessageMapping 으로 라우팅된다.
        registry.setApplicationDestinationPrefixes("/app");
    }

}
