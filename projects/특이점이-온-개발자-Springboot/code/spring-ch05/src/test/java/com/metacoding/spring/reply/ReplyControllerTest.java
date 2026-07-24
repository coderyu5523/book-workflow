package com.metacoding.spring.reply;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;
import org.springframework.transaction.annotation.Transactional;
import tools.jackson.databind.ObjectMapper;
import com.metacoding.spring.core.util.JwtUtil;
import com.metacoding.spring.user.User;

@Transactional
@AutoConfigureMockMvc
@SpringBootTest
public class ReplyControllerTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper om;

    private String ssarToken; // reply id 1 의 작성자 (user id 1)
    private String cosToken;  // 작성자가 아님 (user id 2)

    @BeforeEach
    void setUp() {
        ssarToken = JwtUtil.create(User.builder().id(1).username("ssar").build());
        cosToken = JwtUtil.create(User.builder().id(2).username("cos").build());
    }

    @Test
    public void save_test() throws Exception {
        ReplyRequest.SaveDTO reqDTO = new ReplyRequest.SaveDTO("새댓글", 1);
        String body = om.writeValueAsString(reqDTO);

        ResultActions actions = mvc.perform(post("/api/replies")
                .content(body).contentType(MediaType.APPLICATION_JSON)
                .header("Authorization", ssarToken));

        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.body.comment").value("새댓글"))
                .andExpect(jsonPath("$.body.username").value("ssar"));
    }

    @Test
    public void save_without_token_test() throws Exception {
        ReplyRequest.SaveDTO reqDTO = new ReplyRequest.SaveDTO("새댓글", 1);
        String body = om.writeValueAsString(reqDTO);

        ResultActions actions = mvc.perform(post("/api/replies")
                .content(body).contentType(MediaType.APPLICATION_JSON));

        actions.andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.status").value(401));
    }

    @Test
    public void deleteById_test() throws Exception {
        // reply id 1 은 ssar(user1)의 댓글
        ResultActions actions = mvc.perform(delete("/api/replies/1")
                .header("Authorization", ssarToken));

        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value(200));
    }

    @Test
    public void delete_not_owner_test() throws Exception {
        // cos 가 ssar 의 댓글(id 1) 삭제 시도 -> 403
        ResultActions actions = mvc.perform(delete("/api/replies/1")
                .header("Authorization", cosToken));

        actions.andExpect(status().isForbidden())
                .andExpect(jsonPath("$.status").value(403));
    }
}
