package com.reflection.ex03;

import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)// 실행 시 발동
@Target(ElementType.METHOD)

public @interface RequestMapping {  // 어노테이션
    String uri() ; //identify

}