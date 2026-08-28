package com.reflection.ex02;

import java.lang.reflect.Method;

public class App {
    public static void main(String[] args) {

        String uri = "/update";
        BoardController boardController = new BoardController();

        Method[] methods = boardController.getClass().getDeclaredMethods();
        for (Method method : methods) {
            RequestMapping rm = method.getDeclaredAnnotation(RequestMapping.class);
            if(rm != null && rm.uri().equals(uri)){  //어노테이션이 붙어 있고 uri이 같다면 호출
                try {
                    method.invoke(boardController); // 리플렉션으로 호출
                    break; 
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }
}