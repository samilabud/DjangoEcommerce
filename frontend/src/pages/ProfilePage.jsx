// src/pages/ProfilePage.jsx
import React, { useEffect, useState } from "react";
import { useAuth } from "@clerk/clerk-react";
import { useApi } from "../api/useApi";
import { UserProfile } from "@clerk/clerk-react";

export default function ProfilePage() {
  const api = useApi();
  const { isLoaded } = useAuth();
  const [showProfile, setShowProfile] = useState(false);

  useEffect(() => {
    if (!isLoaded) return; // espera a que Clerk esté listo

    setShowProfile(true);
  }, [api, isLoaded]);

  if (!showProfile) return <div>Are you logged in?</div>;
  return (
    <div>
      <UserProfile />
    </div>
  );
}
