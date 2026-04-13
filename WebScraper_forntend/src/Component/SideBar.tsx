import { useState } from "react";
import { NavLink } from "react-router-dom";

export default function SideBar() {
  const opts = [
    { name: "Home", icon: "bi bi-house", path: "/Home" },
    { name: "Chat", icon: "bi bi-chat", path: "/Chat" },
    { name: "History", icon: "bi bi-clock-history", path: "/History" },
  ];

  const [isOpen, setIsOpen] = useState(false);

  return (
    <div
      className={`flex flex-col justify-between h-screen bg-gray-900 text-white shadow-xl transition-all duration-500 ease-in-out ${
        isOpen ? "w-56" : "w-16"
      }`}>
      {/* --- Top Section (Toggle + Title) --- */}
      <div>
        <div
          className="flex items-center justify-between p-3 border-b border-gray-700 cursor-pointer"
          onClick={() => setIsOpen((prev) => !prev)}>
          {/* App title - only visible when open */}
          <span
            className={`font-semibold text-lg whitespace-nowrap transition-all duration-300 overflow-hidden ${
              isOpen ? "opacity-100 max-w-[150px]" : "opacity-0 max-w-0"
            }`}>
            AI Panel
          </span>

          {/* Toggle Button */}
          <button
            onClick={() => setIsOpen((prev) => !prev)}
            className="text-xl text-gray-300 hover:text-white cursor-pointer"
            title="Toggle sidebar">
            <i
              className={`bi ${
                isOpen ? "bi-layout-sidebar-inset" : "bi-layout-sidebar"
              } transition-transform duration-300`}></i>
          </button>
        </div>

        {/* --- Navigation Links --- */}
        <nav className="flex flex-col gap-2 mt-3">
          {opts.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 p-3 mx-2 rounded-md transition-all duration-300 ${
                  isActive
                    ? "bg-green-600 text-white"
                    : "text-gray-400 hover:bg-gray-800 hover:text-white"
                }`
              }>
              <i className={`text-xl ${item.icon}`}></i>
              <span
                className={`whitespace-nowrap overflow-hidden transition-all duration-300 ${
                  isOpen ? "opacity-100 max-w-[200px]" : "opacity-0 max-w-0"
                }`}>
                {item.name}
              </span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* --- Bottom Profile Section --- */}
      <div className="p-3 border-t border-gray-700">
        <NavLink
          to="/profile"
          className={({ isActive }) =>
            `flex items-center gap-3 p-2 rounded-md transition-all duration-300 ${
              isActive
                ? "bg-green-600 text-white"
                : "text-gray-400 hover:bg-gray-800 hover:text-white"
            }`
          }>
          <i className="bi bi-person-circle text-2xl"></i>
          <span
            className={`whitespace-nowrap overflow-hidden transition-all duration-300 ${
              isOpen ? "opacity-100 max-w-[200px]" : "opacity-0 max-w-0"
            }`}>
            Profile
          </span>
        </NavLink>
      </div>
    </div>
  );
}
