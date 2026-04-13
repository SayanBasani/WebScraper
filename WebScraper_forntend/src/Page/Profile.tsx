import { useStorage } from "@/Storage/Storage";
import { useNavigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";

export default function Profile() {
  const {
    isLoading,
    isAuthenticated,
    logout: auth0Logout,
    user,
  } = useAuth0();

  const { isDarkMode } = useStorage();
  const navigate = useNavigate();

  const handleLogout = () => {
    auth0Logout({
      logoutParams: { returnTo: window.location.origin },
    });
  };

  // 🔄 Auth loading
  if (isLoading) {
    return (
      <div className={`h-screen flex items-center justify-center ${isDarkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-black"}`}>
        <div className="animate-pulse text-lg">Loading authentication...</div>
      </div>
    );
  }

  // 🔒 Not logged in
  if (!isAuthenticated) {
    return (
      <div className={`h-screen flex items-center justify-center ${isDarkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-black"}`}>
        <div className="text-lg">Please log in to view your profile.</div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${isDarkMode ? "bg-gray-900 text-white" : "bg-gray-50 text-black"}`}>
      
      {/* 🔥 Header */}
      <div className="w-full px-6 py-4 flex justify-between items-center backdrop-blur-md bg-white/10 border-b border-white/10">
        <h1 className="text-2xl font-bold tracking-wide">Profile Dashboard</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg text-white transition"
        >
          Logout
        </button>
      </div>

      {/* 🔥 Main */}
      <div className="max-w-5xl mx-auto px-4 py-10 grid md:grid-cols-3 gap-6">

        {/* 🧑 Profile Card */}
        <div className={`col-span-1 p-6 rounded-2xl shadow-xl backdrop-blur-md border ${isDarkMode ? "bg-gray-800/60 border-gray-700" : "bg-white/80 border-gray-200"}`}>
          
          <div className="flex flex-col items-center">
            <img
              src={user?.picture}
              alt="profile"
              className="w-28 h-28 rounded-full border-4 border-blue-500 shadow-lg object-cover"
            />

            <h2 className="mt-4 text-xl font-semibold">
              {user?.given_name || user?.name} {user?.family_name || ""}
            </h2>

            <p className="text-sm text-gray-400">{user?.email}</p>

            <button
              onClick={() => navigate("/edit-profile")}
              className="mt-4 w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-xl text-white transition"
            >
              Edit Profile
            </button>
          </div>
        </div>

        {/* 📊 Info */}
        <div className="col-span-2 grid gap-6">

          {/* Account Info */}
          <div className={`p-6 rounded-2xl shadow-lg ${isDarkMode ? "bg-gray-800" : "bg-white"}`}>
            <h3 className="text-lg font-semibold mb-3">Account Info</h3>

            <div className="grid sm:grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-400">First Name</p>
                <p className="font-medium">{user?.given_name || "-"}</p>
              </div>

              <div>
                <p className="text-gray-400">Last Name</p>
                <p className="font-medium">{user?.family_name || "-"}</p>
              </div>

              <div>
                <p className="text-gray-400">Email</p>
                <p className="font-medium">{user?.email}</p>
              </div>

              <div>
                <p className="text-gray-400">Status</p>
                <p className="text-green-500 font-medium">Active</p>
              </div>
            </div>
          </div>

          {/* Activity */}
          <div className={`p-6 rounded-2xl shadow-lg ${isDarkMode ? "bg-gray-800" : "bg-white"}`}>
            <h3 className="text-lg font-semibold mb-3">Activity</h3>

            <div className="text-sm text-gray-400 space-y-1">
              <p>✔ Logged in successfully</p>
              <p>✔ Auth0 session active</p>
              <p>✔ Profile loaded</p>
            </div>
          </div>

        </div>
      </div>

      {/* Footer */}
      <div className="text-center text-sm text-gray-400 pb-6">
        © {new Date().getFullYear()} WebScraper. All rights reserved.
      </div>
    </div>
  );
}