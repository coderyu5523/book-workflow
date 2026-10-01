package com.metacoding.spring.core.handler.ex;

// 요청이 잘못됐을 때 (HTTP 400)
public class Exception400 extends RuntimeException {
    public Exception400(String message) {
        super(message);
    }
}
