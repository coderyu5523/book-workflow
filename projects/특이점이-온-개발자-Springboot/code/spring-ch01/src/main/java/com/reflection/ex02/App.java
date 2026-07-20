package com.reflection.ex02;

import java.lang.reflect.Method;

public class App {
    public static void main(String[] args) {
        String uri  = "/update";

        BoardController boardController = new BoardController();

        Method[] methods = boardController.getClass().getDeclaredMethods();
        for (Method method : methods) {
            RequestMapping rm = method.getDeclaredAnnotation(RequestMapping.class);
            if(rm.uri().equals(uri)){  //외부에서 들어온 uri이 같다면 메서드 호출
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