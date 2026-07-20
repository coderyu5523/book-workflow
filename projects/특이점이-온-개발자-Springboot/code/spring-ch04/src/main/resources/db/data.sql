insert into user_tb (username,password,email,created_at) values ('ssar','$2y$04$0yDwb5VSijD7z8Wj3lFlwu50bcZRkUwqZQWekol9g.h1eCEto02VK','ssar@metacoding.com',now());
insert into user_tb (username,password,email,created_at) values ('cos','$2y$04$0yDwb5VSijD7z8Wj3lFlwu50bcZRkUwqZQWekol9g.h1eCEto02VK','cos@metacoding.com',now());

insert into board_tb (title, content, created_at,user_id) values ('title1', 'content1', now(),1); 
insert into board_tb (title, content, created_at,user_id) values ('title2', 'content2', now(),1); 
