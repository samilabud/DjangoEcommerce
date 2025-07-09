// src/components/Navbar.jsx
import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <nav className="p-4 flex space-x-4">
      <Link to="/">Inicio</Link>
      <Link to="/protected">Protegido</Link>
      <Link to="/sign-in">Iniciar Sesión</Link>
      <Link to="/sign-up">Registrarse</Link>
      <Link to="/profile">Perfil</Link>
      <Link to="/products">Productos</Link>
    </nav>
  );
}
