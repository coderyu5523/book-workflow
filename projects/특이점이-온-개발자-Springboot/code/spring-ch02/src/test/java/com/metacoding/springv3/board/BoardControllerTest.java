package com.metacoding.springv3.board;

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
public class BoardControllerTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper om;

    @Test
    public void findAll_test() throws Exception {
        // when
        ResultActions actions = mvc.perform(get("/api/boards"));
        // then
        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value(200))
                .andExpect(jsonPath("$.msg").value("성공"))
                .andExpect(jsonPath("$.body[0].title").value("title1"))
                .andExpect(jsonPath("$.body[1].content").value("content2"));
    }

    @Test
    public void detail_test() throws Exception {
        // when
        ResultActions actions = mvc.perform(get("/api/boards/1"));
        // then
        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.body.id").value(1))
                .andExpect(jsonPath("$.body.title").value("title1"));
    }

    @Test
    public void save_test() throws Exception {
        // given
        BoardRequest.SaveDTO reqDTO = new BoardRequest.SaveDTO("새제목", "새내용");
        String requestBody = om.writeValueAsString(reqDTO);
        // when
        ResultActions actions = mvc.perform(
                post("/api/boards").content(requestBody).contentType(MediaType.APPLICATION_JSON));
        // then
        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.body.title").value("새제목"))
                .andExpect(jsonPath("$.body.content").value("새내용"));
    }

    @Test
    public void update_test() throws Exception {
        // given
        BoardRequest.UpdateDTO reqDTO = new BoardRequest.UpdateDTO("수정제목", "수정내용");
        String requestBody = om.writeValueAsString(reqDTO);
        // when
        ResultActions actions = mvc.perform(
                put("/api/boards/1").content(requestBody).contentType(MediaType.APPLICATION_JSON));
        // then
        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.body.title").value("수정제목"));
    }

    @Test
    public void deleteById_test() throws Exception {
        // when
        ResultActions actions = mvc.perform(delete("/api/boards/1"));
        // then
        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value(200));
    }
}
