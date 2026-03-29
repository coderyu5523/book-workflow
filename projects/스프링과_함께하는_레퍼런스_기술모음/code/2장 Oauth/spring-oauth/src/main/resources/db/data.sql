insert into user_tb(username, password, email, created_at) values('ssar', '1234', 'ssar@nate.com', now());
insert into user_tb(username, password, email, created_at) values('cos', '1234', 'cos@nate.com', now());

insert into post_tb(title, content, user_id, created_at) values('첫 번째 글', '첫 번째 글의 내용입니다.', 1, now());
insert into post_tb(title, content, user_id, created_at) values('두 번째 글', '두 번째 글의 내용입니다.', 2, now());
insert into post_tb(title, content, user_id, created_at) values('세 번째 글', '세 번째 글의 내용입니다.', 1, now());
