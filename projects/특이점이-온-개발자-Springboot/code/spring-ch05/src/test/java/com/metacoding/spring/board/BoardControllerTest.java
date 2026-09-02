package com.metacoding.spring.board;

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
public class BoardControllerTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper om;

    private String ssarToken; // 게시글 작성자 (user id 1)
    private String cosToken;  // 작성자가 아님 (user id 2)

    @BeforeEach
    void setUp() {
        ssarToken = JwtUtil.create(User.builder().id(1).username("ssar").build());
        cosToken = JwtUtil.create(User.builder().id(2).username("cos").build());
    }

    @Test
    public void findAll_test() throws Exception {
        // 목록은 공개 (토큰 불필요)
        ResultActions actions = mvc.perform(get("/api/boards"));
        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value(200))
                .andExpect(jsonPath("$.body[0].title").value("title1"));
    }

    @Test
    public void detail_test() throws Exception {
        ResultActions actions = mvc.perform(get("/api/boards/1"));
        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.body.title").value("title1"))
                .andExpect(jsonPath("$.body.username").value("ssar"))
                .andExpect(jsonPath("$.body.isOwner").value(false));
    }

    @Test
    public void detail_notfound_test() throws Exception {
        // when : 존재하지 않는 게시글
        ResultActions actions = mvc.perform(get("/api/boards/999"));
        // then : 404 + Resp 에러 포맷
        actions.andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.msg").value("게시글을 찾을 수 없습니다"));
    }

    @Test
    public void detail_owner_test() throws Exception {
        // 작성자 토큰으로 상세 -> isOwner true
        ResultActions actions = mvc.perform(get("/api/boards/1")
                .header("Authorization", ssarToken));
        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.body.isOwner").value(true));
    }

    @Test
    public void save_test() throws Exception {
        BoardRequest.SaveDTO reqDTO = new BoardRequest.SaveDTO("새제목", "새내용");
        String requestBody = om.writeValueAsString(reqDTO);

        ResultActions actions = mvc.perform(post("/api/boards")
                .content(requestBody).contentType(MediaType.APPLICATION_JSON)
                .header("Authorization", ssarToken));

        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.body.title").value("새제목"));
    }

    @Test
    public void save_without_token_test() throws Exception {
        // 토큰 없이 쓰기 -> 401
        BoardRequest.SaveDTO reqDTO = new BoardRequest.SaveDTO("새제목", "새내용");
        String requestBody = om.writeValueAsString(reqDTO);

        ResultActions actions = mvc.perform(post("/api/boards")
                .content(requestBody).contentType(MediaType.APPLICATION_JSON));

        actions.andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.status").value(401));
    }


    @Test
    public void update_test() throws Exception {
        // 작성자(ssar)가 자신의 글 수정
        BoardRequest.UpdateDTO reqDTO = new BoardRequest.UpdateDTO("수정제목", "수정내용");
        String requestBody = om.writeValueAsString(reqDTO);

        ResultActions actions = mvc.perform(put("/api/boards/1")
                .content(requestBody).contentType(MediaType.APPLICATION_JSON)
                .header("Authorization", ssarToken));

        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.body.title").value("수정제목"));
    }

    @Test
    public void delete_not_owner_test() throws Exception {
        // 작성자가 아닌 cos 가 삭제 시도 -> 403
        ResultActions actions = mvc.perform(delete("/api/boards/1")
                .header("Authorization", cosToken));

        actions.andExpect(status().isForbidden())
                .andExpect(jsonPath("$.status").value(403));
    }

    @Test
    public void deleteById_test() throws Exception {
        // 작성자(ssar) 삭제 성공
        ResultActions actions = mvc.perform(delete("/api/boards/1")
                .header("Authorization", ssarToken));

        actions.andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value(200));
    }
}
