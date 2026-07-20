# 1. 스프링의 마법: Dispatcher와 리플렉션

> **리플렉션(Reflection)은 스프링에서 클래스, 메서드, 필드 정보를 읽고 수정·호출할 수 있는 기능**
> 
> 
> **입니다. 이를 통해 코드를 미리 알지 못해도 동적으로 객체 생성이나 메서드 실행이 가능합니다.**
> 

이 책은 IDE 프로그램으로 **CURSOR** 를 사용합니다.

# 1.1 자바 프로젝트 생성

자바 사용을 위한 확장 프로그램을 설치하겠습니다.

상단 탭 **View > Extensions**를 선택합니다.

![**1.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image.png)

**1.png**

확장 프로그램 중 **Extension Pack for java**를 검색해 설치합니다.

![**2.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image%201.png)

**2.png**

설치가 완료되면 상단 탭 **View > Command Palette**를 선택합니다.

![**3.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image%202.png)

**3.png**

Command Palette에서 **Java: Create Java Project**를 선택합니다.

![**4.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image%203.png)

**4.png**

다음의 설정으로 자바 프로젝트를 생성합니다

> **project type : No build tools
project name : springv1-intro**
> 

생성된 프로젝트의 구조를 확인할 수 있습니다.

![**5.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image%204.png)

**5.png**

App.java 파일에 main 메서드가 있습니다. main 메서드는 프로젝트 실행 시 가장 먼저 호출됩니다.

**src/App.java**

```java
public class App {
    public static void main(String[] args) throws Exception {
        System.out.println("Hello, World!");
    }
}
```

자바 프로젝트를 실행해보겠습니다. main 메서드에 위치한 Run 혹은 IDE 프로그램의 Run을 통해 프로젝트를 실행합니다.

![**6.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image%205.png)

**6.png**

프로젝트 실행하면 콘솔 창에 Hello, World! 를 확인할 수 있습니다.

![**7.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image%206.png)

**7.png**

<aside>
💡

**자바 프로젝트는 main 메서드를 통해 실행됩니다. 다음 장의 Github 예제처럼 하나의 패키지 안에 여러 개의 프로젝트와 main 메서드가 있다면, 실행하려는 프로젝트의 main 메서드를 선택해 실행해야 합니다.**

</aside>

# 1.2 **Dispatcher와 Controller의 역할**

아래의 Github 주소의 파일 구조와 코드를 참고해 작성합니다.

```java
https://github.com/metacoding-06-springboot-v1/springv1-intro
```

다음과 같이 BoardController를 생성합니다. 내부에 insert, delete, update 메서드가 있습니다.

**ex01/BoardController.java**

```java
package com.reflection.ex01;

public class BoardController {

    public void insert(){
        System.out.println("insert 호출됨");
    }
    public void delete(){
        System.out.println("delete 호출됨");
    }
    public void update(){
        System.out.println("update 호출됨");
    }
}
```

다음으로 main 메서드를 아래와 같이 작성합니다.

main 메서드는 URI라는 변수에 값을 받아 if문을 통해 BorderController 의 메서드로 라우팅 합니다. 

**ex01/App.java**

```java
package com.reflection.ex01;

public class App {
    public static void main(String[] args) {
        String uri  = "/insert";

        BoardController boardController = new BoardController(); // 객체 생성

        if(uri.equals("/insert")){
            boardController.insert();
        }else if(uri.equals("/update")){
            boardController.update();
        }else if(uri.equals("/delete")){
            boardController.delete();
        }
    }
}
```

URI값이 “/insert”이므로, BoardController의 insert 메서드가 호출됩니다.

실행 시 insert 메서드가 호출되는 것을 확인할 수 있습니다.

![**8.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image%207.png)

**8.png**

만약 개발자가 BoardController에  select() 함수를 추가하려면 어떻게 해야 할까요?

**ex01/BoardController.java**

```java
public void select(){
    System.out.println("select 호출됨");
}
```

당연히 main 메서드에도 if 문을 통한 라우팅 처리를 해주어야 합니다. 

<aside>
💡

**프레임워크 입장에서는 개발자가 어떤 메서드를 만들지 알 수 없고, 개발자가 메서드를 추가할 때 마다 프레임워크를 수정해야 합니다. 그래서 동적으로 처리를 위해 리플렉션이 필요한 것입니다.**

</aside>

# 1.3 **리플렉션으로 코드 찾기**

RequestMapping.java 를 생성합니다. RequestMapping 는 URI 값을 받는 커스텀 어노테이션입니다.

> **스프링에서 어노테이션(Annotation)은 특별한 동작을 하는 표시입니다. 실행 시 리플렉션으로 이를 읽어 객체 생성, 요청 매핑, 설정 적용 등 필요한 동작을 자동으로 수행합니다.**
> 

**ex02/RequestMapping.java**

```java
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
```

생성한 어노테이션을 BoardController 에 적용합니다.

if 문으로 처리하던  URI 값을 어노테이션의 속성값으로 사용합니다.

**ex02/BoardController.java**

```java
package com.reflection.ex02;

public class BoardController {

    @RequestMapping(uri = "/insert")
    public void insert(){
        System.out.println("insert 호출됨");
    }
    @RequestMapping(uri = "/delete")
    public void delete(){
        System.out.println("delete 호출됨");
    }
    @RequestMapping(uri = "/update")
    public void update(){
        System.out.println("update 호출됨");
    }
    @RequestMapping(uri = "/select")
    public void select(){
        System.out.println("select 호출됨");
    }

}
```

main 메서드를 아래와 같이 수정합니다.

getDeclaredMethods() 를 사용해 BoardController의 모든 메서드를 가져온 후, @RequestMapping 어노테이션의 URI 값을 비교해 메서드를 실행합니다.

**ex02/App.java**

```java
package com.reflection.ex02;

import java.lang.reflect.Method;

public class App {
    public static void main(String[] args) {
        String uri  = "/update";

        BoardController boardController = new BoardController(); // 객체 생성

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
```

실행 시 update() 메서드가 실행됩니다.

![**9.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image%208.png)

**9.png**

이번에는 개발자가 컨트롤러에 create 메서드를 추가한다면 어떻게 될까요??

**ex02/BoardController.java**

```java
    @RequestMapping(uri = "/create")
    public void create(){
        System.out.println("create 호출됨");
    }
```

이제는 컨트롤러에 메서드만 추가하면 URI 값을 비교해 정확한 메서드가 호출될 것입니다.

# 1.4 **IoC와 DI 실습**: **ComponentScan**

> **컴포넌트 스캔(Component Scan)은 스프링이 특정 어노테이션(@Component, @Service, @Controller, @Repository 등)이 붙은 클래스를 자동으로 찾아 객체를 생성하고 관리하는 기능입니다. 이를 통해 개발자는 직접 객체를 생성하지 않아도 필요할 때 꺼내서 사용할 수 있습니다.**
> 

커스텀 어노테이션 Controller.java 를 생성합니다. Controller 어노테이션은 클래스나 인터페이스에서 사용 가능하도록 설정합니다. 

**ex03/Controller.java**

```java
package com.reflection.ex03;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE) // 클래스, 인터페이스 등에서 사용 가능
public @interface Controller {
}
```

BoardController에 커스텀 어노테이션 @Controller를 사용합니다. @Controller가 붙은 클래스를 찾아 객체를 생성하는 것이 목적입니다.

**ex03/BoardController .java**

```java
package com.reflection.ex03;

@Controller
public class BoardController {

    @RequestMapping(uri = "/insert")
    public void insert(){
        System.out.println("insert 호출됨");
    }
    @RequestMapping(uri = "/delete")
    public void delete(){
        System.out.println("delete 호출됨");
    }
    @RequestMapping(uri = "/update")
    public void update(){
        System.out.println("update 호출됨");
    }
    @RequestMapping(uri = "/select")
    public void select(){
        System.out.println("select 호출됨");
    }
    @RequestMapping(uri = "/create")
    public void create(){
        System.out.println("create 호출됨");
    }
}
```

> **GitHub의 ex03 폴더를 참고하여 App.java를 작성합니다. 이때 프로젝트의 실제 폴더 경로에 따라 결과가 조회되지 않을 수 있으므로, 경로를 반드시 확인해야 합니다.**
> 

main 메서드에서는 아래와 같이 작성합니다. 

이번 챕터에서는 BoardController 클래스를 직접 new를 통해 생성하지 않습니다. main 메서드를 통해 클래스 파일 중 어노테이션이 붙은 클래스의 객체를 생성합니다.

**ex03/App.java**

```java
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
        findUri(instances,"/delete");  // URI 입력
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
```

실행하면 delete 가 호출됩니다. 이제 객체를 생성하지 않고 findUri 메서드에 URI 값만 넣어주면 그에 맞는 결과가 반환됩니다.

![**10.png**](1%20%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98%20%EB%A7%88%EB%B2%95%20Dispatcher%EC%99%80%20%EB%A6%AC%ED%94%8C%EB%A0%89%EC%85%98/image%209.png)

**10.png**

<aside>
💡

**복잡해보이지만 핵심은 스프링 프레임워크가 객체를 대신 생성, 관리해준다는 것입니다.
개발자가 할 일은 필요한 클래스에 어노테이션을 붙이고, URI에 맞는 메서드만 작성하면 됩니다.**

</aside>