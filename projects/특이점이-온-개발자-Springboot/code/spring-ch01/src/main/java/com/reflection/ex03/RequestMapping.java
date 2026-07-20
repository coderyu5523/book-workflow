package com.reflection.ex03;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)// 실행 시 발동
@Target(ElementType.METHOD)

public @interface RequestMapping {  // 어노테이션
    String uri() ; //identify

}