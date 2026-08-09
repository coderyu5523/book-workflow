package com.metacoding.spring.core.handler.ex;

// 권한이 없을 때 (HTTP 403)
public class Exception403 extends RuntimeException {
    public Exception403(String message) {
        super(message);
    }
}
