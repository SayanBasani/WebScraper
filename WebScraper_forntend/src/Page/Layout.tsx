import { Navigate, Outlet } from "react-router-dom";
import SideBar from "@/Component/SideBar";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./../App.css";
import "./../index.css";
import { useStorage } from "@/Storage/Storage";
import { useAuth0 } from '@auth0/auth0-react';
import type { JSX } from "react";

function ProtectedRoute({ children }:{children: JSX.Element}) {
  const { isAuthenticated, isLoading } = useAuth0();
  
  if (isLoading) return <div>Loading...</div>;
  
  return isAuthenticated ? children : <Navigate to="/Account" />;
}

export default function Layout() {

  const { isDarkMode } = useStorage();
  // useEffect(()=>{
  //   (async ()=>{
  //     const loggedIn = await isLogin();
  //     setisAuth(loggedIn.data?.username);
  //   })();
  // },[])
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
        <ProtectedRoute>
          <Outlet />
        </ProtectedRoute>
        {/* {isAuth? <Outlet />: <Navigate to={"/Account"}/>} */}
        {/* </div> */}
      </div>
    </div>
  );
}
