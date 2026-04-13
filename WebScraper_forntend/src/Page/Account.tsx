import "bootstrap-icons/font/bootstrap-icons.css";
import "./../App.css";
import "./../index.css";

import { useAuth0 } from "@auth0/auth0-react";

export default function Account() {
  const {
    isLoading,
    isAuthenticated,
    error,
    loginWithRedirect: login,
    logout: auth0Logout,
    user,
  } = useAuth0();

  const signup = () =>
    login({ authorizationParams: { screen_hint: "signup" } });

  const logout = () =>
    auth0Logout({ logoutParams: { returnTo: window.location.origin } });

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900">
        <p className="text-lg text-gray-700 dark:text-white animate-pulse">
          Loading...
        </p>
      </div>
    );
  }
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 p-4">
      <div className="w-full max-w-md bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">

        {isAuthenticated ? (
          <>
            {/* Avatar */}
            <div className="flex flex-col items-center mb-4">
              <img
                src={user?.picture}
                alt="profile"
                className="w-16 h-16 rounded-full mb-2"
              />
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white">
                {user?.name || "User"}
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-300">
                {user?.email}
              </p>
            </div>

            {/* User Data */}
            <div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg text-xs text-gray-800 dark:text-gray-200 max-h-40 overflow-auto mb-4">
              <pre>{JSON.stringify(user, null, 2)}</pre>
            </div>

            {/* Logout */}
            <button
              onClick={logout}
              className="w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg transition"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <h1 className="text-2xl font-bold text-center text-gray-800 dark:text-white mb-4">
              Welcome 👋
            </h1>

            {error && (
              <div className="bg-red-100 text-red-600 text-sm p-2 rounded mb-3">
                {error.message}
              </div>
            )}

            <div className="flex flex-col gap-3">
              <button
                onClick={signup}
                className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg transition"
              >
                Signup
              </button>

              <button
                onClick={() => login()}
                className="w-full bg-green-500 hover:bg-green-600 text-white py-2 rounded-lg transition"
              >
                Login
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}