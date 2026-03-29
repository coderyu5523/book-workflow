package com.metacoding.spring_doker;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class SpringDokerController {

    @GetMapping("/")
    public String hello() {
        return "hello world!.";
    }
}
