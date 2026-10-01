package com.reflection.ex02;

import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)// 실행 시 발동
@Target(ElementType.METHOD) // 메서드에서 사용

public @interface RequestMapping {  // 어노테이션
    String uri() ; //속성값 지정
}