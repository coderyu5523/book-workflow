package com.metacoding.spring.core.handler.ex;

// 인증되지 않았을 때 (HTTP 401)
public class Exception401 extends RuntimeException {
    public Exception401(String message) {
        super(message);
    }
}
