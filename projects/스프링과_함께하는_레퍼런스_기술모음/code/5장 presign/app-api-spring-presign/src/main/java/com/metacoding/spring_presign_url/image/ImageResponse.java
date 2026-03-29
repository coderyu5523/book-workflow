package com.metacoding.spring_presign_url.image;

import java.time.LocalDateTime;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonFormat;

public class ImageResponse {
    public record Item(
            Long id,
            String originalUrl,
            String resizedUrl) {
        public static Item fromEntity(ImageEntity imageEntity) {
            return new Item(
                    imageEntity.getId(),
                    imageEntity.getOriginalUrl(),
                    imageEntity.getResizedUrl());
        }
    }

    public record Items(List<Item> items) {
    }

    public record Detail(
            Long id,
            String uuid,
            String originalUrl,
            String resizedUrl,
            String fileName,
            @JsonFormat(pattern = "yyyy-MM-dd HH:mm") LocalDateTime createdAt) {
        public static Detail fromEntity(ImageEntity imageEntity) {
            return new Detail(
                    imageEntity.getId(),
                    imageEntity.getUuid(),
                    imageEntity.getOriginalUrl(),
                    imageEntity.getResizedUrl(),
                    imageEntity.getFileName(),
                    imageEntity.getCreatedAt());
        }
    }

    public record PresignedUrlResponse(String key, String presignedUrl) {
    }
}
