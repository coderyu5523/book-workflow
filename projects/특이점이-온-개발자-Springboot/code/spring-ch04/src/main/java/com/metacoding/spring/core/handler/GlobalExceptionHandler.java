package com.metacoding.spring.core.handler;

import java.util.stream.Collectors;
import org.springframework.http.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.handler.ex.*;
import com.metacoding.spring.core.util.Resp;

// 예외를 JSON 응답으로 변환하는 전역 핸들러
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception400.class)
    public ResponseEntity<?> ex400(Exception400 e) {
        return Resp.fail(HttpStatus.BAD_REQUEST, e.getMessage());
    }

    @ExceptionHandler(Exception401.class)
    public ResponseEntity<?> ex401(Exception401 e) {
        return Resp.fail(HttpStatus.UNAUTHORIZED, e.getMessage());
    }

    @ExceptionHandler(Exception403.class)
    public ResponseEntity<?> ex403(Exception403 e) {
        return Resp.fail(HttpStatus.FORBIDDEN, e.getMessage());
    }

    @ExceptionHandler(Exception404.class)
    public ResponseEntity<?> ex404(Exception404 e) {
        return Resp.fail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    // @Valid 검증 실패 (표준 방식)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<?> exValid(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldErrors().stream()
                .map(fieldError -> fieldError.getField() + ":" + fieldError.getDefaultMessage())
                .collect(Collectors.joining(", "));
        return Resp.fail(HttpStatus.BAD_REQUEST, msg);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> exUnknown(Exception e) {
        return Resp.fail(HttpStatus.INTERNAL_SERVER_ERROR, "서버 오류가 발생했습니다");
    }
}
