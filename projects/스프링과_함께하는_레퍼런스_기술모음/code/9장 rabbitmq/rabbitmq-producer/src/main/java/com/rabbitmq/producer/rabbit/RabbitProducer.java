package com.rabbitmq.producer.rabbit;

import com.rabbitmq.producer.dto.RabbitDTO;

import lombok.RequiredArgsConstructor;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class RabbitProducer {

    private final RabbitTemplate rabbitTemplate;

    @Value("${rabbit.exchange}")
    private String exchange;

    @Value("${rabbit.routing-key}")
    private String routingKey;

    public void send(RabbitDTO message) {
        rabbitTemplate.convertAndSend(exchange, routingKey, message);
        System.out.println("[RabbitMQ] 메시지 발행 → " + message);
    }
}