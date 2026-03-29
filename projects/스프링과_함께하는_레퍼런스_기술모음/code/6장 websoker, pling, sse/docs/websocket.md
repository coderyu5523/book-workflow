# WebSocket(STOMP) 실습 문서

이 문서는 `websoket` 프로젝트를 기준으로 WebSocket(STOMP) 흐름과 구성 요소를 정리한 교재입니다.
브라우저는 `/ws`로 연결하고, 클라이언트 → 서버는 `/app`, 서버 → 클라이언트는 `/topic` 경로를 사용합니다.

---

## 1. 프로젝트 기본 설정

**경로: src/../build.gradle**
```gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-mustache'
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-websocket'
    developmentOnly 'org.springframework.boot:spring-boot-devtools'

    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
    runtimeOnly 'com.h2database:h2'
}
```
WebSocket, 웹, 템플릿, JPA까지 실습에 필요한 핵심 의존성을 구성합니다.
---

**경로: src/main/resources/application.properties**
```properties
spring.application.name=websocket
server.port=8080

spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.url=jdbc:h2:mem:testdb;MODE=MySQL
spring.datasource.username=sa
spring.datasource.password=

spring.jpa.hibernate.ddl-auto=create
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

spring.h2.console.enabled=true
spring.h2.console.path=/h2-console
```
H2 메모리 DB를 사용하도록 설정하고 기본 포트는 8080으로 유지합니다.
---

**경로: src/main/java/com/metacoding/websocket/WebsocketApplication.java**
```java
package com.metacoding.websocket;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class WebsocketApplication {

    public static void main(String[] args) {
        SpringApplication.run(WebsocketApplication.class, args);
    }
}
```
프로젝트 실행을 시작하는 메인 엔트리 클래스입니다.
---

## 2. WebSocket(STOMP) 설정

**경로: src/main/java/com/metacoding/websocket/config/WebSocketConfig.java**
```java
package com.metacoding.websocket.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

@EnableWebSocketMessageBroker
@Configuration
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
                .setAllowedOriginPatterns("*");
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic");
        registry.setApplicationDestinationPrefixes("/app");
    }
}
```
클라이언트는 `/ws`로 연결하고, `/app`은 서버 처리, `/topic`은 브로커 직통으로 라우팅되도록 구성합니다.
---

## 3. 채팅 도메인

**경로: src/main/java/com/metacoding/websocket/chat/Chat.java**
```java
package com.metacoding.websocket.chat;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Getter
@Table(name = "chat_tb")
@Entity
public class Chat {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String message;

    @Builder
    public Chat(Integer id, String message) {
        this.id = id;
        this.message = message;
    }
}
```
채팅 메시지를 DB에 저장하기 위한 엔티티입니다.
---

**경로: src/main/java/com/metacoding/websocket/chat/ChatRequest.java**
```java
package com.metacoding.websocket.chat;

public record ChatRequest(String message) {
}
```
클라이언트가 전송한 JSON 바디에서 message만 받도록 분리한 요청 모델입니다.
---

**경로: src/main/java/com/metacoding/websocket/chat/ChatRepository.java**
```java
package com.metacoding.websocket.chat;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ChatRepository extends JpaRepository<Chat, Integer> {
}
```
채팅 저장/조회 기능을 스프링 데이터 JPA에 위임하는 리포지토리입니다.
---

**경로: src/main/java/com/metacoding/websocket/chat/ChatService.java**
```java
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
        Chat chat = Chat.builder().message(req.message()).build();
        return chatRepository.save(chat);
    }

    public List<Chat> findAll() {
        Sort desc = Sort.by(Sort.Direction.DESC, "id");
        return chatRepository.findAll(desc);
    }
}
```
저장은 write 트랜잭션으로 처리하고, 조회는 최신 메시지가 먼저 보이도록 정렬합니다.
---

## 4. STOMP + REST 컨트롤러

**경로: src/main/java/com/metacoding/websocket/chat/ChatController.java**
```java
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

    @MessageMapping("/chats")
    public void handle(ChatRequest payload) {
        Chat saved = chatService.save(payload);
        messagingTemplate.convertAndSend("/topic/chats", saved);
    }

    @GetMapping("/chats")
    @ResponseBody
    public List<Chat> findAll() {
        return chatService.findAll();
    }

    @PostMapping("/chats")
    @ResponseBody
    public Chat save(@RequestBody ChatRequest request) {
        if (request == null || request.message() == null) {
            throw new IllegalArgumentException("message is required");
        }
        return chatService.save(request);
    }
}
```
STOMP는 `/app/chats`로 들어온 메시지를 저장한 뒤 `/topic/chats`로 브로드캐스트합니다. REST는 테스트용으로 GET/POST를 제공합니다.
---

## 5. 프론트 화면 (Mustache)

**경로: src/main/resources/templates/index.mustache**
```html
<!doctype html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <title>WebSocket Chat</title>
</head>

<body>
    <h1>WebSocket 실시간 채팅</h1>
    <hr>

    <div>
        <input id="message" placeholder="메시지 입력">
        <button onclick="sendMessage()">전송</button>
    </div>

    <ul id="chat-box"></ul>

    <script src="https://cdn.jsdelivr.net/npm/stompjs@2.3.3/lib/stomp.min.js"></script>
    <script>
        const socketUrl = (location.protocol === "https:" ? "wss://" : "ws://") + location.host + "/ws";
        const stompClient = Stomp.over(new WebSocket(socketUrl));

        stompClient.connect({}, () => {
            stompClient.subscribe("/topic/chats", (frame) => {
                const chat = JSON.parse(frame.body);
                appendChat(chat.message);
            });
        }, (error) => {
            console.error("STOMP 연결 오류:", error);
        });

        function sendMessage() {
            const messageInput = document.getElementById("message");
            const message = messageInput.value.trim();
            if (!stompClient.connected) {
                alert("연결 중입니다. 잠시 후 다시 시도하세요.");
                return;
            }
            stompClient.send("/app/chats", {}, JSON.stringify({ message }));
            messageInput.value = "";
            messageInput.focus();
        }

        function appendChat(message, prepend = true) {
            const box = document.getElementById("chat-box");
            const li = document.createElement("li");
            li.innerText = message;
            prepend ? box.prepend(li) : box.appendChild(li);
        }
    </script>
</body>

</html>
```
브라우저는 `/ws`로 연결하고 `/topic/chats`를 구독해 메시지를 받으며, 전송은 `/app/chats`로 보냅니다.
---

## 6. 실행 방법

- 실행: `./gradlew bootRun`
- 접속: `http://localhost:8080/`
- 동작: 브라우저 여러 개를 띄우고 메시지를 보내면 즉시 동기화됩니다.
