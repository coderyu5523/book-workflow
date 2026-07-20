package com.metacoding.springv3.core.handler;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import com.metacoding.springv3.core.handler.ex.*;
import com.metacoding.springv3.core.util.Resp;

// 예외를 JSON 응답으로 변환하는 전역 핸들러
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception404.class)
    public ResponseEntity<?> ex404(Exception404 e) {
        return Resp.fail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> exUnknown(Exception e) {
        return Resp.fail(HttpStatus.INTERNAL_SERVER_ERROR, "서버 오류가 발생했습니다");
    }
}
