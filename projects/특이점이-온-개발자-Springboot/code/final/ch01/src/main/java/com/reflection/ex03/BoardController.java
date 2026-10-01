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