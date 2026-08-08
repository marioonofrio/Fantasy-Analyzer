import { Link } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../context/AuthContext";
import { googleLogin } from "../api/players";

function Nav() {
  const { user, login, logout } = useAuth();

  return (
    <nav>
      <Link to="/">Players</Link> | <Link to="/trade">Trade Calculator</Link> | <Link to="/league">Import League</Link>
      {" | "}
      {user ? (
        <span>{user.name} <button onClick={logout}>Log out</button></span>
      ) : (
        <GoogleLogin
          onSuccess={async (credentialResponse) => {
            if (!credentialResponse.credential) return;
            const data = await googleLogin(credentialResponse.credential);
            login(data.access_token, { user_id: data.user_id, email: data.email, name: data.name });
          }}
          onError={() => console.error("Google login failed")}
        />
      )}
    </nav>
  );
}

export default Nav;