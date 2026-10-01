package com.reflection.ex03;

import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE) 
public @interface Controller {
}
