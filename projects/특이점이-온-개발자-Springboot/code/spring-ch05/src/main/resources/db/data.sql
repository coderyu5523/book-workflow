insert into user_tb (username,password,email,created_at) values ('ssar','1234','ssar@metacoding.com',now());
insert into user_tb (username,password,email,created_at) values ('cos','1234','cos@metacoding.com',now());

insert into board_tb (title, content, created_at,user_id) values ('title1', 'content1', now(),1); 
insert into board_tb (title, content, created_at,user_id) values ('title2', 'content2', now(),1); 

insert into reply_tb(comment,board_id,user_id,created_at) values('comment1',1,1,now());
insert into reply_tb(comment,board_id,user_id,created_at) values('comment2',1,1,now());
insert into reply_tb(comment,board_id,user_id,created_at) values('comment3',1,2,now());
insert into reply_tb(comment,board_id,user_id,created_at) values('comment4',2,2,now());
