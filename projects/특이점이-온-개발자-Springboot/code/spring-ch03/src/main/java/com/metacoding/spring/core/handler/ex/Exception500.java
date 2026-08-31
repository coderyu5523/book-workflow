package com.metacoding.spring.core.handler.ex;

// 예상 가능한 서버 오류 (500)
public class Exception500 extends RuntimeException {
    public Exception500(String message) {
        super(message);
    }
}
