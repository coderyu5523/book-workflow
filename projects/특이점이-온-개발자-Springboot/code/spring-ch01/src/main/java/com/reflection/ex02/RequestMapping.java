package com.reflection.ex02;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)// 실행 시 발동
@Target(ElementType.METHOD) // 메서드에서 사용

public @interface RequestMapping {  // 어노테이션
    String uri() ; //속성값 지정
}