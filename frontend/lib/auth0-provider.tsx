"use client";

import { ReactNode } from "react";

interface AuthProviderWrapperProps {
  children: ReactNode;
}

export function AuthProviderWrapper({ children }: AuthProviderWrapperProps) {
  // Simple wrapper - no Auth0 needed
  return <>{children}</>;
}
