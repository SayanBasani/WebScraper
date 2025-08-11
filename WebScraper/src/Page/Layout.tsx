import { Navigate, Outlet } from "react-router-dom";
import SideBar from "@/Component/SideBar";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./../App.css";
import "./../index.css";
import { useStorage } from "@/Storage/Storage";

export default function Layout() {
  const { isDarkMode,isAuth } = useStorage();

  return (
    <div
      className={`${
        isDarkMode ? " bg-gray-900 text-white " : " bg-white text-black "
      } w-screen h-screen flex`}>
      <div className={`border-r-1 border-gray-700`}>
        <SideBar />
      </div>
      <div className="w-full h-screen flex flex-col gap-3">
        <div className="flex-grow overflow-auto p-3">
         {isAuth? <Outlet />: <Navigate to={"/Account"}/>}
        </div>
      </div>
    </div>
  );
}
