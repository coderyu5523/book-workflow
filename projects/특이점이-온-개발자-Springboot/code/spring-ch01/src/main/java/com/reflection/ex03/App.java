package com.reflection.ex03;

import java.io.File;
import java.lang.reflect.Method;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.*;

public class App {

    // 패키지 내부의 class 파일을 찾음
    public static void main(String[] args) throws URISyntaxException, ClassNotFoundException, InstantiationException, IllegalAccessException {

        ClassLoader classLoader = Thread.currentThread().getContextClassLoader(); 
        URL packageUrl = classLoader.getResource("com/reflection/ex03"); // 폴더의 어노테이션을 분석

        File ex03 = new File(packageUrl.toURI());

        List<Object> instances = new ArrayList<>();

        File[] files = ex03.listFiles();
        for(File file : files){  
            System.out.println("파일명: " + file.getName());
            if(file.getName().endsWith(".class")){  // 이름의 끝이 .class 면 실행
                String className = "com.reflection.ex03"+"."+file.getName().replace(".class",""); // .class 를 공백으로 처리 .CLASS가 있으면 NEW 를 못함
                Class cls = Class.forName(className);  
                // 어노테이션이 있는지 확인
                if (cls.isAnnotationPresent(Controller.class)){ 
                    System.out.println("어노테이션이 있는 클래스 : " + file.getName());
                    Object instance = cls.newInstance(); // 객체 생성
                    instances.add(instance); 
                }
            }
        }
        System.out.println("--------------------------------");
        findUri(instances,"/delete");
    }
   
    // uri 를 비교해 메서드 호출
    public static void findUri(List<Object> instances,String uri){

        for(Object instance : instances){
            Method[] methods = instance.getClass().getDeclaredMethods(); 
            for (Method method : methods) {
                RequestMapping rm = method.getDeclaredAnnotation(RequestMapping.class);
                if(rm.uri().equals(uri)){  
                    try {
                        method.invoke(instance);  
                        break; 
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }

            }
        }

    }
}