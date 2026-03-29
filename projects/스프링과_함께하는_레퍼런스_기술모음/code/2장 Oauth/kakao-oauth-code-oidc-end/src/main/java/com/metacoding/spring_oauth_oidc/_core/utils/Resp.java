package com.metacoding.spring_oauth_oidc._core.utils;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import lombok.Data;

@Data
public class Resp<T> {

    // 응답 상태 코드(보통 200, 400, 401, 500 등)
    private Integer status;

    // 사용자에게 보여줄 메시지(성공/실패 이유 등)
    private String msg;

    // 실제 응답 데이터(제네릭 타입으로 어떤 DTO든 담을 수 있음)
    private T body;

    public Resp(Integer status, String msg, T body) {
        this.status = status;
        this.msg = msg;
        this.body = body;
    }

    /**
     * 성공 응답(기본 메시지 = "성공")
     * - 컨트롤러에서 return Resp.ok(dto); 처럼 쓰기 좋습니다.
     */
    public static <B> ResponseEntity<Resp<B>> ok(B body) {
        return ok("성공", body);
    }

    /**
     * 성공 응답(메시지 커스텀 가능)
     * - HTTP 상태 코드는 200(OK)로 내려줍니다.
     * - Resp 내부 status도 200으로 맞춰둡니다.
     */
    public static <B> ResponseEntity<Resp<B>> ok(String msg, B body) {
        // 공통 응답 포맷 생성
        Resp<B> resp = new Resp<>(200, msg, body);

        // HTTP 응답까지 200 OK로 감싸서 반환
        return new ResponseEntity<>(resp, HttpStatus.OK);
    }
}
