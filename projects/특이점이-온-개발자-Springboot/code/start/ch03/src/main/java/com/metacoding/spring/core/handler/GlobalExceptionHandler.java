package com.metacoding.spring.core.handler;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.handler.ex.*;
import com.metacoding.spring.core.util.Resp;

// 예외를 JSON 응답으로 변환하는 전역 핸들러
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception400.class)
    public ResponseEntity<?> exApi400(Exception400 e) {
        // TODO : 실습 4 - 전역 예외 처리
        return null;
    }

    @ExceptionHandler(Exception401.class)
    public ResponseEntity<?> exApi401(Exception401 e) {
        // TODO : 실습 4 - 전역 예외 처리
        return null;
    }

    @ExceptionHandler(Exception403.class)
    public ResponseEntity<?> exApi403(Exception403 e) {
        // TODO : 실습 4 - 전역 예외 처리
        return null;
    }

    @ExceptionHandler(Exception404.class)
    public ResponseEntity<?> exApi404(Exception404 e) {
        // TODO : 실습 4 - 전역 예외 처리
        return null;
    }

    @ExceptionHandler(Exception500.class)
    public ResponseEntity<?> exApi500(Exception500 e) {
        // TODO : 실습 4 - 전역 예외 처리
        return null;
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> exUnKnown(Exception e) {
        // TODO : 실습 4 - 전역 예외 처리
        return null;
    }
}
