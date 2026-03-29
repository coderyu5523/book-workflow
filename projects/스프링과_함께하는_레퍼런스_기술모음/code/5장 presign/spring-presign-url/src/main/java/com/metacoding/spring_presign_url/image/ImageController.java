package com.metacoding.spring_presign_url.image;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class ImageController {

    private final ImageService imageService;

    @PostMapping("/presigned")
    public ImageResponse.PresignedUrlResponse presign(@RequestBody ImageRequest.PresignRequest reqDTO) {
        return imageService.generatePresignedUrl(reqDTO);
    }

    @GetMapping("/list")
    public ImageResponse.Items getAllImages() {
        return imageService.listAll();
    }

    @GetMapping("/{id}")
    public ImageResponse.Detail getImageDetail(@PathVariable Long id) {
        return imageService.findById(id);
    }

    @PostMapping("/complete")
    public ImageResponse.Detail complete(@RequestBody ImageRequest.completeRequest reqDTO) {
        return imageService.checkAndSave(reqDTO);
    }

}
