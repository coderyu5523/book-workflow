package com.reflection.ex01;

public class App {
    public static void main(String[] args) {
        String uri = "/insert";

        BoardController boardController = new BoardController();

        if(uri.equals("/insert")){
            boardController.insert();
        }else if(uri.equals("/update")){
            boardController.update();
        }else if(uri.equals("/delete")){
            boardController.delete();
        }
    }
}