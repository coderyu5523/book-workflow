package com.rabbitmq.producer.config;

import org.springframework.amqp.core.*;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

// RabbitMQ 교환기, 큐, 라우팅키를 스프링 Bean으로 등록
@Configuration
public class RabbitConfig {

    @Value("${rabbit.exchange}")
    private String exchangeName;

    @Value("${rabbit.queue}")
    private String queueName;

    @Value("${rabbit.routing-key}")
    private String routingKey;

     // Jackson2 기반 JSON 컨버터 등록
    @Bean
    public MessageConverter jsonMessageConverter() {
        return new Jackson2JsonMessageConverter();
    }

    @Bean
    public DirectExchange exchange() {
        return new DirectExchange(exchangeName, true, false);
    }

    @Bean
    public Queue queue() {
        return QueueBuilder.durable(queueName).build();
    }

    @Bean
    public Binding binding(Queue queue, DirectExchange exchange) {
        return BindingBuilder.bind(queue).to(exchange).with(routingKey);
    }
}
