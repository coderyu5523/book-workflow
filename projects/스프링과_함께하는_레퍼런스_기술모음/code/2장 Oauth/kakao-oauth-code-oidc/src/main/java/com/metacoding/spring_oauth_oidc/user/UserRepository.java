package com.metacoding.spring_oauth_oidc.user;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Integer> {

    Optional<User> findByProviderAndProviderId(String provider, String providerId);
}
