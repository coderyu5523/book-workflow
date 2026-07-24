package com.metacoding.spring.core.handler.ex;

// 자원을 찾을 수 없을 때 (HTTP 404)
public class Exception404 extends RuntimeException {
    public Exception404(String message) {
        super(message);
    }
}
