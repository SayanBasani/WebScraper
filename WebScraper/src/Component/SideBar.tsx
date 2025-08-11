import { useState } from "react";
import { NavLink } from "react-router-dom";

export default function SideBar() {
  const opts = [
    { name: "Home", icon: "bi bi-house", path: "/Home" },
    { name: "Chat", icon: "bi bi-chat", path: "/Chat" },
    { name: "History", icon: "bi bi-clock-history", path: "/History" },
    { name: "Profile", icon: "bi bi-person", path: "/Profile" },
    { name: "Logout", icon: "bi bi-box-arrow-right", path: "/Logout" },
  ];

  const [toggleSideBar, setToggleSideBar] = useState(false);
  const [showText, setShowText] = useState(true);

  const handleToggle = () => {
    if (toggleSideBar) {
      // Sidebar is closing — hide text immediately
      setShowText(false);
      setToggleSideBar(false);
    } else {
      // Sidebar is opening — open sidebar first, then show text
      setToggleSideBar(true);
      setTimeout(() => {
        setShowText(true);
      }, 500); // match sidebar animation duration
    }
  };

  return (
    <div
      className={` ${toggleSideBar?" 220px ":" 45px "} m-2 grid gap-3 transition-all ease-in-out duration-500 overflow-hidden`}>
      <div className="w-full bg-green-700 overflow-hidden rounded-[5px]">
        <button
          onClick={handleToggle}
          type="button"
          className="w-full"
          title="toggle sidebar">
          <i className="bi bi-layout-sidebar"></i>
        </button>
      </div>
      <div className="w-full grid gap-3 px-3 py-2">
        {opts.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex gap-3 cursor-pointer ${
                isActive ? "text-blue-500" : "text-gray-400 hover:text-gray-600"
              }`
            }>
            <i className={`text-xl ${item.icon}`}></i>
            <div
              className={`${
                toggleSideBar ? "" : "hidden"
              } flex gap-3 items-center`}>
              <span
                className={`text-lg transition-all duration-300 ease-in-out overflow-hidden whitespace-nowrap ${
                  showText ? "opacity-100 max-w-[200px]" : "opacity-0 max-w-0"
                }`}>
                {item.name}
              </span>
            </div>
          </NavLink>
        ))}
      </div>
    </div>
  );
}
