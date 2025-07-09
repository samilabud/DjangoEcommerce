// src/App.jsx
import { Routes, Route, Navigate } from "react-router-dom";
import {
  SignIn,
  SignUp,
  SignedIn,
  SignedOut,
  RedirectToSignIn,
  UserButton,
} from "@clerk/clerk-react";
import HomePage from "./pages/HomePage";
import ProtectedPage from "./pages/ProtectedPage";
import ProfilePage from "./pages/ProfilePage";
import ProductsPage from "./pages/ProductsPage";

export default function App() {
  return (
    <>
      <header className="p-4 bg-gray-100 flex justify-between">
        <h1 className="text-xl">Mi E-Commerce</h1>
        <UserButton /> {/* Muestra avatar / sign-out cuando está logueado */}
      </header>

      <Routes>
        {/* Páginas públicas */}
        <Route path="/" element={<HomePage />} />

        {/* Clerk: Sign In */}
        <Route
          path="/sign-in/*"
          element={<SignIn routing="path" path="/sign-in" />}
        />
        {/* Clerk: Sign Up */}
        <Route
          path="/sign-up/*"
          element={<SignUp routing="path" path="/sign-up" />}
        />

        {/* Rutas protegidas */}
        <Route
          path="/protected"
          element={
            <SignedIn>
              <ProtectedPage />
            </SignedIn>
          }
        />
        <Route
          path="/profile"
          element={
            <SignedIn>
              <ProfilePage />
            </SignedIn>
          }
        />
        <Route
          path="/products"
          element={
            <SignedIn>
              <ProductsPage />
            </SignedIn>
          }
        />
        {/* Si no estás firmado, redirige a /sign-in */}
        <Route
          path="/protected"
          element={
            <SignedOut>
              <RedirectToSignIn />
            </SignedOut>
          }
        />

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </>
  );
}
