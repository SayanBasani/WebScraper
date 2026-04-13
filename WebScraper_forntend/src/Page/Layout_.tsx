import { Navigate, Outlet } from "react-router-dom";
import SideBar from "@/Component/SideBar";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./../App.css";
import "./../index.css";
import { useStorage } from "@/Storage/Storage";
import { useEffect } from "react";
import { isLogin } from "@/Storage/BackendRequests";

export default function Layout() {
  const { isDarkMode, isAuth, setisAuth } = useStorage();
  useEffect(()=>{
    (async ()=>{
      const loggedIn = await isLogin();
      setisAuth(loggedIn.data?.username);
    })();
  },[])
  return (
    <div
      className={`${
        isDarkMode ? " bg-gray-900 text-white " : " bg-white text-black "
      } w-screen h-screen flex`}>
      <div className={` h-screen border-r-1 border-gray-700`}>
        <SideBar />
      </div>
      <div className="w-full h-screen flex flex-col gap-3">
        {/* <div className="h-screen flex-grow overflow-auto p-3"> */}
         {isAuth? <Outlet />: <Navigate to={"/Account"}/>}
        {/* </div> */}
      </div>
    </div>
  );
}
