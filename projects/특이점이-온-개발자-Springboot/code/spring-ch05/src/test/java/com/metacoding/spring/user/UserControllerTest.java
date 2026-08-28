package com.metacoding.spring.user;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;
import org.springframework.transaction.annotation.Transactional;
import tools.jackson.databind.ObjectMapper;

@Transactional
@AutoConfigureMockMvc
@SpringBootTest
public class UserControllerTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper om;

    @Test
    public void join_test() throws Exception {
        UserRequest.SaveDTO reqDTO = new UserRequest.SaveDTO("newuser", "1234", "newuser@metacoding.com");
        String body = om.writeValueAsString(reqDTO);

        ResultActions actions = mvc.perform(post("/join")
                .content(body).contentType(MediaType.APPLICATION_JSON));

        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value(200));
    }

    @Test
    public void login_test() throws Exception {
        // 시드 계정 ssar / 1234
        UserRequest.LoginDTO reqDTO = new UserRequest.LoginDTO("ssar", "1234");
        String body = om.writeValueAsString(reqDTO);

        ResultActions actions = mvc.perform(post("/login")
                .content(body).contentType(MediaType.APPLICATION_JSON));

        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value(200))
                .andExpect(jsonPath("$.body").exists()); // JWT 토큰 발급
    }

    @Test
    public void login_wrong_password_test() throws Exception {
        UserRequest.LoginDTO reqDTO = new UserRequest.LoginDTO("ssar", "wrong");
        String body = om.writeValueAsString(reqDTO);

        ResultActions actions = mvc.perform(post("/login")
                .content(body).contentType(MediaType.APPLICATION_JSON));

        actions.andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.status").value(401));
    }
}
