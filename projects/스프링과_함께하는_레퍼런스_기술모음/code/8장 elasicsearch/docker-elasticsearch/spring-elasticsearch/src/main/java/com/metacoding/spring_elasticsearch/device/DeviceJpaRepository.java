package com.metacoding.spring_elasticsearch.device;

import org.springframework.data.jpa.repository.JpaRepository;

public interface DeviceJpaRepository extends JpaRepository<DeviceEntity, Long> {
}