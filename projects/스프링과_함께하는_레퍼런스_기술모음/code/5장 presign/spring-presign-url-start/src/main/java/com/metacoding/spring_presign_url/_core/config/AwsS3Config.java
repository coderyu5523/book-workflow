package com.metacoding.spring_presign_url._core.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.presigner.S3Presigner;

/**
 * AWS S3 설정 파일
 * - AWS 자격증명(AccessKey, SecretKey)을 application.properties에서 주입받는다.
 * - S3Client와 S3Presigner를 Bean으로 등록한다.
 * - Presigned URL 생성은 S3Presigner가 수행한다.
 */
@Configuration
public class AwsS3Config {

    
}