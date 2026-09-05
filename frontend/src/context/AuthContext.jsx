import { createContext, useContext, useEffect, useState } from "react";
import { api } from "../api";

const AuthContext = createContext({
  user: null,
  login: () => {},
  logout: () => {},
  showLoginModal: false,
  setShowLoginModal: () => {},
});

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("chronoflow_user");
    return saved ? JSON.parse(saved) : null;
  });
  const [showLoginModal, setShowLoginModal] = useState(false);

  useEffect(() => {
    if (user) {
      localStorage.setItem("chronoflow_user", JSON.stringify(user));
    } else {
      localStorage.removeItem("chronoflow_user");
    }
  }, [user]);

  async function loginWithGoogle(payload) {
    try {
      const res = await api.loginGoogle(payload);
      setUser(res);
      setShowLoginModal(false);
      return res;
    } catch (err) {
      console.error("Google Auth Error:", err);
      throw err;
    }
  }

  function logout() {
    setUser(null);
    localStorage.removeItem("chronoflow_user");
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        loginWithGoogle,
        logout,
        showLoginModal,
        setShowLoginModal,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
